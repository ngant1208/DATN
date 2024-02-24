CREATE DATABASE Nhan_vien;

CREATE TABLE Nhan_vien.dbo.ttnv(
	MaNV nvarchar(10) PRIMARY KEY,
	Ten nvarchar(30) NULL,
	Ngaysinh date NULL,
	Gioitinh nvarchar(10) NULL,
	CCCD nvarchar(20) NOT NULL,
	Pwd nvarchar(10) NOT NULL,
	SDT nvarchar(20) NULL,
);

INSERT INTO Nhan_vien.dbo.ttnv(MaNV,Ten,Ngaysinh,Gioitinh,CCCD,Pwd,SDT)
VALUES
    ('NV100','Nguyen Thi Nga','2000/01/29','Female','123983023748','123456','0345871905'),
    ('NV101','Tran Thi Thu','1999/11/01','Female','384628459263','038430','0975437449'),
    ('NV102','Vu Van Bao','2000/03/12','Male','40358238647','394834','0368592949'),
	('NV103','Ta Thu Thuy','1998/06/03','Female','93745284637','982470','0983561086'),
	('NV104','Le Van Son','2001/09/26','Male','294537492628','039847','0273674899'),
	('NV105','Dinh Thu Huong','1998/12/06','Female','836483673829','038490','0268902700'),
	('NV106','Tran Van Tuan','1996/01/19','Male','094635262738','037648','0385957483')
	;

