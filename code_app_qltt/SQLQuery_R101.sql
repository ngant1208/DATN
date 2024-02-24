CREATE DATABASE R101;

CREATE TABLE R101.DBO.ttphong(
	Sophong nvarchar(10) PRIMARY KEY,
	Trangthai BIT NOT NULL,
	Loai nvarchar(20) NULL,
	Gia INT NULL,
);

INSERT INTO R101.DBO.ttphong(Sophong,Trangthai,Loai,Gia)
VALUES
    (101,1,'STD',600000)
;

CREATE TABLE R101.dbo.ttkh(
	  TenKH nvarchar(20) NULL,
      Ngaysinh date NULL,
      Gioitinh nvarchar(10) NULL,
      CCCD nvarchar(20) PRIMARY KEY,
      SDT nchar(20) NULL,
      Ngaythue date NOT NULL,
      Ngaytra date NOT NULL,
      Sophong nvarchar(10) NULL,
      Hinh1 varbinary(MAX) NULL,
      Hinh2 varbinary(MAX) NULL,
      Hinh3 varbinary(MAX) NULL,
      Hinh4 varbinary(MAX) NULL,
      Hinh5 varbinary(MAX) NULL,
	  CONSTRAINT ttkh_ttphong
	  FOREIGN KEY (Sophong)
	  REFERENCES R101.dbo.ttphong(Sophong)
);