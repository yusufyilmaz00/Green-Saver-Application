-- Drop existing tables and sequence if they exist
DROP TABLE IF EXISTS invoice CASCADE;
DROP TABLE IF EXISTS subscriberContact CASCADE;
DROP TABLE IF EXISTS corporateSubscriber CASCADE;
DROP TABLE IF EXISTS individualSubscriber CASCADE;
DROP TABLE IF EXISTS Subscriber CASCADE;
DROP TABLE IF EXISTS energy CASCADE;
DROP SEQUENCE IF EXISTS sub_no_seq;
DROP SEQUENCE IF EXISTS invoice_no_seq;


-- Ana 'Subscriber' tablosu (Genel Abone Tablosu)
CREATE TABLE Subscriber (
    subscriptionNo integer not null,
    subscriberType char(1) check (subscriberType IN ('I', 'C')), -- 'I' = Individual, 'C' = Corporate
	userpassword VARCHAR(20) not null,
    primary key (subscriptionNo)
);

--Bireysel Aboneler
CREATE TABLE individualSubscriber (
    subscriptionNo integer not null,
    fname varchar(30) not null,
    lname varchar(30) not null,
    idNumber char(11) not null,
    birthday date not null,
    registrationDate date,
    primary key (subscriptionNo),
    foreign key (subscriptionNo) references Subscriber(subscriptionNo) on delete cascade,
    CHECK (birthday <= CURRENT_DATE - INTERVAL '18 years') -- 18 yaş sınırı
);


-- Kurumsal Aboneler
CREATE TABLE corporateSubscriber (
    subscriptionNo integer not null,
    corporateName varchar(40) not null,
    taxNo char(10) not null,
    corporateType varchar(40) not null,
    foundationDate date not null,
    registerDate date not null,
    primary key (subscriptionNo),
    foreign key (subscriptionNo) references Subscriber(subscriptionNo) on delete cascade
);

-- Abone İletişim Bilgileri
CREATE TABLE subscriberContact (
    subscriptionNo integer not null,
    address varchar(100),
    email varchar(50),
    phoneNumber char(10),
    primary key (subscriptionNo),
    foreign key (subscriptionNo) references Subscriber(subscriptionNo) on delete cascade
);

-- Enerji Fiyatlandırması
CREATE TABLE energy (
    invoiceType varchar(15),
    corporationPrice numeric,
    individualPrice numeric,
    carbonEmission numeric,
    primary key (invoiceType)
);

-- Fatura Tablosu
CREATE TABLE invoice (
    invoiceDate date,
    invoiceNo integer not null,
    subNumber integer not null,
    invoiceType varchar(15),
    consumptionAmount numeric,
    invoiceAmount numeric,
    primary key (invoiceNo),
    foreign key (subNumber) references Subscriber(subscriptionNo),
    foreign key (invoiceType) references energy(invoiceType)
);

-- Abone Numarası İçin Sıralama
CREATE SEQUENCE sub_no_seq
    START WITH 100000000
    INCREMENT BY 1
    MAXVALUE 999999999
    NO CYCLE;

-- Fatura Numarası İçin Sıralama
CREATE SEQUENCE invoice_no_seq
    START WITH 200000000
    INCREMENT BY 1
    MAXVALUE 999999999
    NO CYCLE;

DROP FUNCTION insert_individual_subscriber(
    fname VARCHAR,
    lname VARCHAR,
    id_number CHAR(11),
    birthday DATE,
    registration_date DATE,
    address VARCHAR,
    email VARCHAR,
    phone_number CHAR(10),
	userpass VARCHAR
);

CREATE OR REPLACE FUNCTION insert_individual_subscriber(
    fname VARCHAR,
    lname VARCHAR,
    id_number CHAR(11),
    birthday DATE,
    registration_date DATE,
    address VARCHAR,
    email VARCHAR,
    phone_number CHAR(10),
	userpass VARCHAR
) RETURNS INTEGER AS $$
DECLARE
    sub_no integer;
BEGIN
    INSERT INTO Subscriber (subscriptionNo, subscriberType,userpassword)
    VALUES (NEXTVAL('sub_no_seq'), 'I',userpass)
    RETURNING subscriptionNo INTO sub_no;

    INSERT INTO individualSubscriber (subscriptionNo, fname, lname, idNumber, birthday, registrationDate)
    VALUES (sub_no, fname, lname, id_number, birthday, registration_date);

    INSERT INTO subscriberContact (subscriptionNo, address, email, phoneNumber)
    VALUES (sub_no, address, email, phone_number);
	
	RETURN sub_no;
END;
$$ LANGUAGE plpgsql;

-- Function to insert a single corporate subscriber and populate contact table
CREATE OR REPLACE FUNCTION insert_corporate_subscriber(
    corporate_name VARCHAR(40),
    tax_no CHAR(10),
    corporate_type VARCHAR,
    foundation_date DATE,
    register_date DATE,
    address VARCHAR,
    email VARCHAR,
    phone_number CHAR(10),
	userpass VARCHAR
) RETURNS INTEGER AS $$
DECLARE
    sub_no integer;
BEGIN
    INSERT INTO Subscriber (subscriptionNo, subscriberType,userpassword)
    VALUES (NEXTVAL('sub_no_seq'), 'C',userpass)
    RETURNING subscriptionNo INTO sub_no;

    INSERT INTO corporateSubscriber (subscriptionNo, corporateName, taxNo, corporateType, foundationDate, registerDate)
    VALUES (sub_no, corporate_name, tax_no, corporate_type, foundation_date, register_date);

    INSERT INTO subscriberContact (subscriptionNo, address, email, phoneNumber)
    VALUES (sub_no, address, email, phone_number);

	RETURN sub_no;
END;
$$ LANGUAGE plpgsql;

-- Function to insert a single invoice
CREATE OR REPLACE FUNCTION insert_invoice(
    invoiceDate date,
    subNumber integer,
    invoiceType varchar(15),
    consumptionAmount numeric,
    invoiceAmount numeric
) RETURNS VOID AS $$
BEGIN
    INSERT INTO invoice (invoiceDate,invoiceNo, subNumber, invoiceType, consumptionAmount, invoiceAmount)
    VALUES (invoiceDate,NEXTVAL('invoice_no_seq'), subNumber, invoiceType, consumptionAmount, invoiceAmount);
END;
$$ LANGUAGE plpgsql;

CREATE FUNCTION invoice_collision_func() 
RETURNS TRIGGER AS $$
BEGIN
    -- Aynı tarih ve aynı fatura türü varsa kontrol et
    IF EXISTS (
        SELECT 1 
        FROM invoice
        WHERE invoiceDate = NEW.invoiceDate 
          AND invoiceType = NEW.invoiceType
    ) THEN
        -- Eğer böyle bir kayıt varsa hata fırlat
        RAISE EXCEPTION 'You cannot insert the same invoice on the same date and type';
        RETURN NULL;
    ELSE
        -- Eğer problem yoksa yeni kaydı kabul et
        RETURN NEW;
    END IF; 
END; 
$$ LANGUAGE 'plpgsql';

CREATE TRIGGER invoice_collision_trig 
BEFORE INSERT
ON invoice 
FOR EACH ROW 
EXECUTE PROCEDURE invoice_collision_func();

CREATE TYPE carbon_emission_record AS (
    invoice_no INTEGER,
    invoice_date DATE,
    carbon_emission NUMERIC
);
CREATE OR REPLACE FUNCTION calculate_carbon_emission(p_subscriptionNo INTEGER)
RETURNS SETOF carbon_emission_record AS $$
DECLARE
    emission_record carbon_emission_record; -- Record tipi bir değişken tanımlıyoruz
BEGIN
    FOR emission_record IN
        SELECT 
            i.invoiceNo AS invoice_no,
            i.invoiceDate AS invoice_date,
            i.consumptionAmount * e.carbonEmission AS carbon_emission
        FROM 
            invoice i
        INNER JOIN 
            energy e
        ON 
            i.invoiceType = e.invoiceType
        WHERE 
            i.subNumber = p_subscriptionNo
    LOOP
        RETURN NEXT emission_record; -- Her bir kaydı döndür
    END LOOP;
END;
$$ LANGUAGE plpgsql;

CREATE VIEW all_sub_view 
AS
SELECT i.subscriptionno, fname || ' ' || lname AS subName, s.subscribertype 
FROM individualsubscriber i join subscriber s on i.subscriptionno=s.subscriptionno
union
SELECT c.subscriptionno,corporatename, s.subscribertype 
FROM corporatesubscriber c join subscriber s on c.subscriptionno=s.subscriptionno
order by subscriptionno;


CREATE OR REPLACE FUNCTION trig_invoiceInsertControl()
RETURNS TRIGGER AS $$
BEGIN
	IF NOT EXISTS (SELECT 1 FROM subscriber s WHERE new.subnumber = s.subscriptionNo )
		THEN RAISE EXCEPTION 'No subscriber found with subscription no %',new.subnumber;
	END IF;
	RETURN NEW;
END;
$$ LANGUAGE plpgsql;


CREATE TRIGGER trig_invoiceInsertControl
BEFORE INSERT 
ON invoice
FOR EACH ROW EXECUTE FUNCTION trig_invoiceInsertControl();

CREATE OR REPLACE FUNCTION get_all_individualInvoices(subscriberNo integer)
RETURNS void AS $$
DECLARE
 individual_cursor CURSOR FOR SELECT subscriptionNo, invoiceNo, fname|| ' '|| lname AS subscriberName,invoiceDate,invoiceType,consumptionAmount,invoiceAmount
 					    FROM invoice i1,individualSubscriber i2
						WHERE i1.subnumber = i2.subscriptionNo and subscriberNo = i1.subnumber;
 BEGIN
	FOR row_i IN individual_cursor LOOP
	 RAISE INFO '%, %, %, %, %, %, % ',row_i.subscriptionNo,row_i.invoiceNo,row_i.subscriberName,row_i.invoiceDate,row_i.invoiceType,row_i.consumptionAmount,row_i.invoiceAmount;
	END LOOP;
 END;
 $$ LANGUAGE plpgsql;

 CREATE OR REPLACE FUNCTION get_all_corporateInvoices(subscriberNo integer)
RETURNS void AS $$
DECLARE
 corporate_cursor CURSOR FOR SELECT subscriptionNo, invoiceNo, corporateName AS subscriberName,invoiceDate,invoiceType,consumptionAmount,invoiceAmount
 					    FROM invoice i1,corporateSubscriber i2
						WHERE i1.subnumber = i2.subscriptionNo and subscriberNo = i1.subnumber;
 BEGIN
	FOR row_i IN corporate_cursor LOOP
	 RAISE INFO '%, %, %, %, %, %, % ',row_i.subscriptionNo,row_i.invoiceNo,row_i.subscriberName,row_i.invoiceDate,row_i.invoiceType,row_i.consumptionAmount,row_i.invoiceAmount;
	END LOOP;
 END;
 $$ LANGUAGE plpgsql;



