#code by XiangYu Fan PB18000006
Drop Database lab1;
Create Database lab1;
Use lab1;
#Book（ID: char(8)， name:varchar(10)， 
#author:varchar(10)， price:float， status: int）
#图书号 ID 为主键，书名不能为空。状态（status）
#为 1 表示书被借出， 0 表示在馆，默认值为 0。
Create Table Book(
	ID Char(8),
    name VarChar(100) NOT NULL,#这里是为了可以正常insert助教给的样例
    author VarChar(10),
    price float,
    status int Default 0,
    Constraint CK_B Check (status IN (0,1)),
    #Constraint CK_N Check (status IS NOT NULL),
    Constraint PK_B Primary Key(ID)
);
#Reader（ID:char(8)， name:varchar(10)， 
#age:int， address:varchar(20)） 
#读者号ID为主键
Create Table Reader(
	ID Char(8),
    name VarChar(10),
    age int,
    address VarChar(20),
	Constraint PK_R Primary Key(ID)
);
#Borrow（book_ID:char(8)， Reader_ID:char(8)， 
#Borrow_Date:date，Return_Date:date） 
#还期 Return_Date 为 NULL 表示该书未还。主键为（图书号，
#读者号），图书号为外键，引用图书表的图书号，读者号为外键，
#引用读者表的读者号。
Create Table Borrow(
	book_ID Char(8),
    Reader_ID Char(8),
    Borrow_Date date,
    Return_Date date,
    Constraint PK_Bo Primary Key(book_ID,Reader_ID),
    Constraint FK_Bo_0 Foreign Key(book_ID) References Book(ID),
    Constraint FK_Bo_1 Foreign Key(Reader_ID) References Reader(ID)
);
#2.设计例子，验证实体完整性、参照完整性、用户自定义完整性
#实体完整性，关系模式的主码不可为空
#insert into Book value(NULL, 'Python从入门到精通', 'AABB', 99.0, 1);
#insert into Reader value(NULL, '范翔宇', 18, '少年班学院');
#insert into Borrow value('b1', NULL, '2021-04-02', NULL);
#insert into Borrow value(NULL, 'r3', '2021-04-02', NULL);
#insert into Borrow value(NULL, NULL, '2021-04-02', NULL);
#参照完整性，R的任一非空FK值都在S的CK中有一个相同的值
#insert into Borrow value('b20','r3','2021-04-02', NULL);
#insert into Borrow value('b3','r30','2021-04-02', NULL);
#insert into Borrow value(NULL,'r3','2021-04-02', NULL);
#insert into Borrow value('b3',NULL,'2021-04-02', NULL);
#用户自定义完整性
#insert into Book value('b13', 'Python从入门到精通', 'AABB', 99.0, 3);
# 插入书籍
insert into Book value('b1', '数据库系统实现', 'Ullman', 59.0, 1);
insert into Book value('b2', '数据库系统概念', 'Abraham', 59.0, 1);
insert into Book value('b3', 'C++ Primer', 'Stanley', 78.6, 1);
insert into Book value('b4', 'Redis设计与实现', '黄建宏', 79.0, 1);
insert into Book value('b5', '人类简史', 'Yuval', 68.00, 0);
insert into Book value('b6', '史记(公版)', '司马迁', 220.2, 1);
insert into Book value('b7', 'Oracle Database 编程艺术', 'Thomas', 43.1, 1);
insert into Book value('b8', '分布式数据库系统及其应用', '邵佩英', 30.0, 0);
insert into Book value('b9', 'Oracle 数据库系统管理与运维', '张立杰', 51.9, 0);
insert into Book value('b10', '数理逻辑', '汪芳庭', 22.0, 0);
insert into Book value('b11', '三体', '刘慈欣', 23.0, 1);
insert into Book value('b12', 'Fluent python', 'Luciano', 354.2, 1);

# 插入读者
insert into Reader value('r1', '李林', 18, '中国科学技术大学东校区');
insert into Reader value('r2', 'Rose', 22, '中国科学技术大学北校区');
insert into Reader value('r3', '罗永平', 23, '中国科学技术大学西校区');
insert into Reader value('r4', 'Nora', 26, '中国科学技术大学北校区');
insert into Reader value('r5', '汤晨', 22, '先进科学技术研究院');
#自己加的
insert into Reader value('r6', 'JAY', 23, '中国科学技术大学西校区');

# 插入借书
insert into Borrow value('b5','r1',  '2021-03-12', '2021-04-07');
insert into Borrow value('b6','r1',  '2021-03-08', '2021-03-19');
insert into Borrow value('b11','r1',  '2021-01-12', NULL);

insert into Borrow value('b3', 'r2', '2021-02-22', NULL);
insert into Borrow value('b9', 'r2', '2021-02-22', '2021-04-10');
insert into Borrow value('b7', 'r2', '2021-04-11', NULL);

insert into Borrow value('b1', 'r3', '2021-04-02', NULL);
insert into Borrow value('b2', 'r3', '2021-04-02', NULL);
insert into Borrow value('b4', 'r3', '2021-04-02', '2021-04-09');
insert into Borrow value('b7', 'r3', '2021-04-02', '2021-04-09');

insert into Borrow value('b6', 'r4', '2021-03-31', NULL);
insert into Borrow value('b12', 'r4', '2021-03-31', NULL);

insert into Borrow value('b4', 'r5', '2020-04-10', NULL);
#3.1检索读者 Rose 的读者号和地址；
Select ID, address 
From Reader 
Where name = 'Rose';
#3.2检索读者 Rose 所借阅读书（包括已还和未还图书）的图书名和借期；
Select Book.name, Borrow.Borrow_Date 
From Book, Reader, Borrow
Where Book.ID = Borrow.book_ID and Reader.ID = Borrow.Reader_ID
and Reader.name = 'Rose';
#3.3检索未借阅图书的读者姓名
Select name
From Reader
Where Reader.ID NOT IN(Select Distinct Reader_ID From Borrow);
#3.4检索 Ullman 所写的书的书名和单价
Select name, price
From Book
Where author = 'Ullman';
#3.5检索读者“李林”借阅未还的图书的图书号和书名；
Select Book.ID, Book.name
From Book, Reader, Borrow
Where Reader.name = '李林' and Book.ID = Borrow.book_ID and 
Reader.ID = Borrow.Reader_ID and Borrow.Return_Date IS NULL;
#3.6检索借阅图书数目超过 3 本的读者姓名；
Select a.name
From Reader a, (
Select COUNT(*) AS Borrow_num, Reader_ID AS ID
From Borrow
Group By Borrow.Reader_ID
Having COUNT(*) > 3) b
Where a.ID = b.ID;
#3.7检索没有借阅读者“李林”所借的任何一本书的读者姓名和读者号；
#TBD
Select name, ID From Reader
Where ID NOT IN(
Select Distinct  Reader.ID
From Reader, Borrow, Book
Where Reader.ID = Borrow.Reader_ID and Book.ID = Borrow.book_ID and Book.ID IN(
Select Book.ID From Borrow, Book, Reader 
Where Borrow.book_ID = Book.ID and Borrow.Reader_ID = Reader.ID 
and Reader.name = '李林'));
#3.8检索书名中包含“Oracle”的图书书名及图书号；
Select name, ID From Book
Where name LIKE '%Oracle%';
#3.9创建一个读者借书信息的视图，该视图包含读者号、姓名、所借图书号、图书名
#和借期； 并使用该视图查询最近一年所有读者的读者号以及所借阅的不同图书数；
Create View Reader_Borrow (rID, rname, bID, bname, bDate) As
Select Reader.ID AS rID, Reader.name AS rname, Book.ID AS bID, Book.name AS bname, Borrow.Borrow_Date AS bDate
From Reader, Book, Borrow
Where Reader.ID = Borrow.Reader_ID and Book.ID = Borrow.book_ID;
Select a.rID, COUNT(a.bID)
From Reader_Borrow a
#最近一年
Where a.bDate >DATE_SUB(CURDATE(), INTERVAL 1 YEAR)
Group By a.rID;
Drop View Reader_Borrow;
#4.设计一个存储过程，实现对 Book 表的 ID 的修改verision
Delimiter //
Drop Procedure IF EXISTS ChangBook //
Create Procedure ChangeBook(IN old_ID Char(8), IN new_ID Char(8))
BEGIN
Declare state int default 0;
Declare rID char(8);
Declare bn Varchar(100);
Declare ba Varchar(10);
Declare bp float;
Declare bs int default 0;
Declare bbd date;
Declare brd date;
Declare continue Handler for SQLEXCEPTION set state = -1;
#当作一个事务处理
Start Transaction;
Select name, author, price, status From book Where ID = old_ID into bn, ba, bp, bs;
insert into book value(new_ID, bn, ba, bp, bs);
Update Borrow
SET book_ID = new_ID
Where book_ID = old_ID;
Delete From book
Where ID = old_ID;
IF state = 0 THEN
	COMMIT;
ELSE 
	ROLLBACK;
END IF;
END
//
Delimiter ;
#测试样例
#set @str1 = 'b1';
#set @str2 = 'b1111';
#call ChangeBook(@str1, @str2);
#select * from Book, Borrow where Book.ID = Borrow.book_ID;
#select * from Book, Borrow where Book.ID = 'b1111' and Borrow.book_ID = 'b1111';
#5.设计一个存储过程，检查每本图书 status 是否正确，并返回 status 不正确的图书数。
Delimiter //
Drop Procedure IF EXISTS CheckStatus //
Create Procedure CheckStatus(OUT counter INT)
BEGIN
Declare state INT DEFAULT 0;
Declare ID1 Char(8);
Declare Status1 INT;
Declare 
	ct CURSOR FOR 
    (Select ID, status From Book
     #已借出，但是Borrow里面没有正在借阅的条目
	 Where 
     #status不满足条件 status为NULL
     (status IS NULL) or
     (status = 1 
		and NOT EXISTS(
			#查询是否有满足条件的borrow记录
			Select * From Borrow 
			Where book_ID = Book.ID and Return_Date IS NULL)
     )or 
     #已还或者未借出，但是Borrow里面有正在借阅的条目
     (status = 0
		and EXISTS(
			select *  From Borrow
			Where book_ID = Book.ID and Return_Date IS NULL)
     )
	);
Declare CONTINUE HANDLER FOR NOT FOUND SET state = 1;
SET counter = 0;
OPEN ct;
REPEAT
	FETCH ct INTO ID1, Status1;
	SET counter = counter + 1;
    UNTIL state = 1
END REPEAT;
#会多一个NULL NULL；
SET counter = counter - 1;
CLOSE ct;
END //
Delimiter ;
#测试样例232-261行
#Update Book 
#SET status = 0
#Where ID = 'b12';
#Update Book 
#SET status = 1
#Where ID = 'b5';
#Update Book
#SET status = NULL
#Where ID = 'b3';
#call CheckStatus(@output);
#Select ID, status From Book
#     #已借出，但是Borrow里面没有正在借阅的条目
#	 Where 
     #status不满足条件 
     #status为NULL的
#     (status IS NULL) or
#     (status = 1 
#		and NOT EXISTS(
#			#查询是否有满足条件的borrow记录
#			Select * From Borrow 
#			Where book_ID = Book.ID and Return_Date IS NULL)
#     )or 
     #已还或者未借出，但是Borrow里面有正在借阅的条目
#     (status = 0
#		and EXISTS(
#			select *  From Borrow
#			Where book_ID = Book.ID and Return_Date IS NULL)
 #    );
#Select ID, status From Book;
#Select @output;
Delimiter //
#6.设计触发器， 实现： 当一本书被借出时，自动将 Book 表中相应图书的 status 修改为
#1；当某本书被归还时，自动将 status 改为 0
Drop Trigger IF EXISTS INSERTModifyStauts //
Create Trigger INSERTModifyStauts
AFTER INSERT
ON Borrow
For Each Row
BEGIN
#Declare RD date;
#Select Return_Date From Borrow Where book_ID = new.book_ID and Reader_ID = new.Reader_ID INTO RD;
IF new.Return_Date IS NULL THEN
UPDATE Book SET status = 1
WHERE ID = new.book_ID;
ELSE 
UPDATE Book SET status = 0
WHERE ID = new.book_ID;
END IF;
END //
Delimiter ;
Delimiter //
Drop Trigger IF EXISTS UPDATEModifyStatus //
Create Trigger UPDATEModifyStauts
AFTER UPDATE
ON Borrow
For Each Row
BEGIN
#Declare RD date;
#Select Return_Date From Borrow Where book_ID = new.book_ID and Reader_ID = new.Reader_ID INTO RD;
IF new.Return_Date IS NULL THEN
UPDATE Book SET status = 1
WHERE ID = new.book_ID;
ELSE 
UPDATE Book SET status = 0
WHERE ID = new.book_ID;
END IF;
END //
Delimiter ;
#测试样例
#insert into Borrow value('b9','r1',  '2021-04-12', NULL);
#Update Borrow 
#SET Return_Date = '2021-04-12'
#Where book_ID = 'b1111' and Reader_ID = 'r1';
#select * from Book;

#drop database lab1;