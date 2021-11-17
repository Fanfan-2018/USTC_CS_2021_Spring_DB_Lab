/*==============================================================*/
/* DBMS name:      MySQL 5.0                                    */
/* Created on:     2021/6/27 19:22:58                           */
/*==============================================================*/
drop database if exists lab3;
create database lab3;
use lab3;

create table bank (
	bankname	VARCHAR(20)		not null,
	city		VARCHAR(20)		not null,
	money		DOUBLE			not null,
	constraint PK_BANK primary key (bankname)
);

create table department (
	departID		CHAR(4)			not null,
    departname		VARCHAR(20)		not null,
    departtype		VARCHAR(15),
    manager			CHAR(18)		not null,
    bank			VARCHAR(20)		not null,
    constraint PK_DEPARTMENT primary key (departID),
	Constraint FK_BANK_DEPART Foreign Key(bank) References bank(bankname)
);

create table employee (
	empID			CHAR(18)		not null,
    empname			VARCHAR(20)		not null,
    empphone		CHAR(11),
    empaddr			VARCHAR(50),
    emptype			CHAR(1),
    empstart		DATE			not null,
    depart			CHAR(4),
    constraint PK_EMPLOYEE primary key (empID),
	Constraint FK_DEPART_EMP Foreign Key(depart) References department(departID),
	Constraint CK_EMPTYPE Check(emptype IN ('0','1'))
);

create table customer (
	cusID			CHAR(18)		not null,
	cusname			VARCHAR(60)		not null,
	cusphone		CHAR(11)		not null,
	address			VARCHAR(50),
	contact_phone	CHAR(11)		not null,
	contact_name	VARCHAR(10)		not null,
	contact_Email	VARCHAR(20),
	relation		VARCHAR(10)		not null,
    loanres			CHAR(18),
    accres			CHAR(18),
	constraint PK_CUSTOMER primary key (cusID),
    Constraint FK_CUS_LOANRES Foreign Key(loanres) References employee(empID),
    Constraint FK_CUS_ACCRES Foreign Key(accres) References employee(empID)
);

create table accounts(
	accountID		CHAR(6)			not null,
	money			DOUBLE			not null,
    settime			DATE		not null,
	accounttype		VARCHAR(10)		not null,	
	constraint PK_ACC primary key (accountID),
	Constraint CK_ACCOUNTTYPE Check(accounttype IN ('save','check'))
);

create table saveacc (
	accountID		CHAR(6)			not null,
    interestrate	float,
    savetype		CHAR(1),
    constraint PK_SAVEACC primary key (accountID),
	Constraint FK_SAVE_ACC Foreign Key(accountID) References accounts(accountID) On Delete Cascade
);

create table checkacc (
	accountID		CHAR(6)			not null, 
    overdraft		DOUBLE,
    constraint PK_CHECKACC primary key (accountID),
	Constraint FK_CHECK_ACC Foreign Key(accountID) References accounts(accountID) On Delete Cascade
);

create table cusforacc (
	accountID		CHAR(6)			not null,
    bank			VARCHAR(20)		not null,
    cusID			CHAR(18)		not null,
    visit			DATE,
    accounttype		VARCHAR(10)		not null,
    constraint PK_CUSACC primary key (accountID, cusID),
    Constraint FK_BANK_ACCOUT Foreign Key(bank) References bank(bankname),
    Constraint FK_CUS Foreign Key(cusID) References customer(cusID),
	Constraint FK_CUS_ACC Foreign Key(accountID) References accounts(accountID) On Delete Cascade,
    Constraint UK Unique Key(bank, cusID, accounttype)
); 

create table loan (
	loanID			CHAR(4)			not null,
    money			DOUBLE			not null,
    bank			VARCHAR(20)		not null,
    state			CHAR(1)			default '0',
    constraint PK_LOAN primary key (loanID),
	Constraint FK_BANK_LOAN Foreign Key(bank) References bank(bankname)
);

create table cusforloan (
	loanID			CHAR(4)			not null,
    cusID			CHAR(18)		not null,
    constraint PK_CUSLOAN primary key (loanID, cusID),
    Constraint FK_LOAN Foreign Key(loanID) References loan(loanID) On Delete Cascade,
    Constraint FK_CUSL Foreign Key(cusID) References customer(cusID)
);

create table payinfo (
	loanID			CHAR(4)			not null,
    cusID			CHAR(18)		not null,
    money			DOUBLE			not null,
    paytime			DATE		not null,
    constraint PK_PAYINFO primary key (loanID, cusID, money, paytime),
    Constraint FK_PAY_LOAN Foreign Key(loanID) References loan(loanID) On Delete Cascade,
    Constraint FK_PAY_CUS Foreign Key(cusID) References customer(cusID)
); 

create view checkaccounts (accountID,money,settime,accounttype,bank,cusID,visit,overdraft)
as select accounts.accountID,money,settime,accounttype,bank,cusID,visit,overdraft 
from accounts,checkacc,(select distinct accounts.accountID,bank,cusID,visit from accounts,cusforacc where accounts.accountID=cusforacc.accountID) tmp 
where accounts.accountID=checkacc.accountID and accounts.accountID=tmp.accountID;

create view saveaccounts (accountID,money,settime,accounttype,bank,cusID,visit,interestrate,savetype)
as select accounts.accountID,money,settime,accounttype,bank,cusID,visit,interestrate,savetype
from accounts,saveacc,(select distinct accounts.accountID,bank,cusID,visit from accounts,cusforacc where accounts.accountID=cusforacc.accountID) tmp 
where accounts.accountID=saveacc.accountID and accounts.accountID=tmp.accountID;

create view savestat (bank,money,cusID,settime)
as select t1.bank,money,cusID,settime 
from (select bank,money,settime from saveaccounts) t1, 
(select bank,cusID from cusforacc where accounttype='save') t2
where t1.bank=t2.bank;

create view checkstat (bank,money,cusID,settime)
as select t1.bank,money,cusID,settime 
from (select bank,money,settime from checkaccounts) t1, 
(select bank,cusID from cusforacc where accounttype='check') t2
where t1.bank=t2.bank;

create view loanstat (bank,money,cusID,paytime)
as select bank,money,cusID,paytime
from (select loanID,bank from loan)t1,
(select loanID,money,paytime,cusID from payinfo) t2
where t1.loanID=t2.loanID;


delimiter $
create trigger loanDelete
Before delete on loan
for each row
begin
	declare a int;
	select state into a from loan where old.loanID=loan.loanID;
    if a = 1 then
		signal sqlstate 'HY000' set message_text = 'Under loan';
	end if;
end $
delimiter ;


delimiter $
create trigger loanState
After insert on payinfo
for each row
begin
	declare pay int;
    declare total int;
	select sum(money) into pay from payinfo where payinfo.loanID=new.loanID;
    select money into total from loan where loan.loanID=new.loanID;
    if pay > 0 and pay < total then
		update loan set state='1' where loan.loanID=new.loanID;
	elseif pay=total then
		update loan set state='2' where loan.loanID=new.loanID;
	elseif pay>total then
		delete from payinfo where payinfo.loanID=new.loanID and payinfo.cusID=new.cusID and payinfo.paytime=new.paytime and payinfo.money=new.money;
		signal sqlstate 'HY001' set message_text = 'Over loan amount';
	end if;
end $
delimiter ;

-- 提前输入到数据库的数据
-- bank
insert into bank values ('Beijing branch','Beijing',8000000);
insert into bank values ('Shanghai branch','Shanghai',5000000);
insert into bank values ('Hefei branch','Hefei',3000000);
-- department
insert into department values ('0001','depart1','type1','000000000000000001','Beijing branch');
insert into department values ('0002','depart2','type2','000000000000000002','Beijing branch');
insert into department values ('0101','depart1','type1','000000000000000003','Shanghai branch');
insert into department values ('0102','depart2','type2','000000000000000004','Shanghai branch');
insert into department values ('0201','depart1','type1','000000000000000005','Hefei branch');
insert into department values ('0202','depart2','type2','000000000000000006','Hefei branch');
-- employee
insert into employee values ('000000000000000001','Wang Gang','13615655155','Beijing1','1','2010-01-01','0001');
insert into employee values ('000000000000000002','Wang Hua','13615655154','Beijing2','1','2012-01-03','0002');
insert into employee values ('000000000000000003','Li Gang','13615655153','Shanghai1','1','2014-03-01','0101');
insert into employee values ('000000000000000004','Li Hua','13615655152','SHanghai2','1','2014-03-01','0102');
insert into employee values ('000000000000000005','Zhao Gang','13615655151','Hefei1','1','2016-03-01','0201');
insert into employee values ('000000000000000006','Zhao Hua','13615655150','Hefei2','1','2016-01-01','0202');
insert into employee values ('000000000000000007','Yuan Jia','13615655145','Beijing3','0','2018-01-01','0001');
insert into employee values ('000000000000000008','Yuan Yi','13615655135','Beijing4','0','2018-02-01','0001');
insert into employee values ('000000000000000009','Yuan Bing','13615655125','SHanghai3','0','2018-03-01','0101');
insert into employee values ('000000000000000010','Yuan Ding','13615655115','Hefei3','0','2019-01-01','0202');

SELECT * FROM customer;
-- 测试用数据，可注释掉
-- customer
insert into customer values ('000000000000000011','Li Yamei','19966525606',null,'19966525606','fxy',null,'family',null,'000000000000000001');
insert into customer values ('000000000000000012','AA BB','19966525606',null,'19966525606','fxy',null,'family',null, '000000000000000002');
insert into customer values ('000000000000000013','DB lab','19966525606',null,'19966525606','fxy',null,'family',null, '000000000000000002');
insert into customer values ('000000000000000014','Just test','19966525606',null,'19966525606','fxy',null,'family',null, '000000000000000002');
insert into customer values ('000000000000000015','胡图图','19966525606',null,'19966525606','fxy',null,'family',null, '000000000000000002');
-- loan
insert into loan values ('0001',100,'Beijing branch','0');
insert into loan values ('0002',100,'Beijing branch','0');
insert into cusforloan values ('0001','000000000000000011');
insert into cusforloan values ('0001','000000000000000012');
insert into cusforloan values ('0002','000000000000000011');

-- accounts
insert into accounts values ('000001',100,'2021-06-26','check');
insert into accounts values ('000002',100,'2021-06-26','save');
insert into saveacc values ('000002',100,'1');
insert into checkacc values ('000001',200);
insert into cusforacc values ('000001','Beijing branch','000000000000000013','2021-06-26','check');
insert into cusforacc values ('000001','Beijing branch','000000000000000012','2021-06-26','check');
insert into cusforacc values ('000002','Beijing branch','000000000000000014','2021-06-26','save');
