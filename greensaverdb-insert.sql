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

-- individual subscribers inserts
SELECT insert_individual_subscriber('Alice', 'Smith', '12345678901', '1995-07-20', '2023-01-01','456 Elm St, Apt 9C, Sample City', 'alice.smith@example.com', '5552345678','123456789');
SELECT insert_individual_subscriber('John', 'Doe', '22345678901', '1990-05-12', '2023-01-02', '789 Maple St, Apt 1A, Los Angeles', 'john.doe@la.com', '5551234567','123456789');
SELECT insert_individual_subscriber('Emily', 'Johnson', '32345678901', '1985-03-08', '2023-01-03', '123 Oak St, Apt 4D, Chicago', 'emily.johnson@chicago.com', '5553456789','123456789');
SELECT insert_individual_subscriber('Michael', 'Brown', '42345678901', '1988-07-15', '2023-01-04', '456 Pine St, Apt 5B, Miami', 'michael.brown@miami.com', '5554567890','123456789');
SELECT insert_individual_subscriber('Sarah', 'Taylor', '52345678901', '1992-11-20', '2023-01-05', '789 Elm St, Apt 6C, Seattle', 'sarah.taylor@seattle.com', '5555678901','123456789');
SELECT insert_individual_subscriber('Chris', 'Davis', '62345678901', '1991-01-10', '2023-01-06', '321 Cedar St, Apt 7E, Boston', 'chris.davis@boston.com', '5556789012','123456789');
SELECT insert_individual_subscriber('Jessica', 'Martinez', '72345678901', '1989-04-25', '2023-01-07', '654 Birch St, Apt 8F, Austin', 'jessica.martinez@austin.com', '5557890123','123456789');
SELECT insert_individual_subscriber('Daniel', 'Garcia', '82345678901', '1994-06-30', '2023-01-08', '987 Willow St, Apt 9G, Denver', 'daniel.garcia@denver.com', '5558901234','123456789');
SELECT insert_individual_subscriber('Laura', 'Hernandez', '92345678901', '1993-09-14', '2023-01-09', '321 Aspen St, Apt 10H, Portland', 'laura.hernandez@portland.com', '5559012345','123456789');
SELECT insert_individual_subscriber('David', 'Clark', '10234567890', '1987-12-05', '2023-01-10', '123 Main St, Apt 3A, San Diego', 'david.clark@sandiego.com', '5556789010','123456789');
SELECT insert_individual_subscriber('Sophia', 'Hall', '11234567890', '1996-03-22', '2023-01-11', '456 Broadway St, Apt 2B, Nashville', 'sophia.hall@nashville.com', '5557890121','123456789');
SELECT insert_individual_subscriber('Olivia', 'Wilson', '12234567890', '1997-09-15', '2023-01-12', '654 Sunset Blvd, Apt 4D, Atlanta', 'olivia.wilson@atlanta.com', '5557893456','123456789');
SELECT insert_individual_subscriber('James', 'Anderson', '13234567890', '1984-04-17', '2023-01-13', '789 River Rd, Apt 2E, Houston', 'james.anderson@houston.com', '5558905678','123456789');


-- corporate subscribers inserts
SELECT insert_corporate_subscriber('Quantum Dynamics', '9234567890', 'Aerospace', '2016-06-12', '2023-01-10', '123 Aviation Blvd, Suite 100, Charlotte', 'contact@quantumdynamics.com', '5559123456','123456789');
SELECT insert_corporate_subscriber('EcoSys', '1034567890', 'Sustainability', '2019-11-25', '2023-01-11', '789 Greenway Dr, Suite 150, Pittsburgh', 'info@ecosys.com', '5559234567','123456789');
SELECT insert_corporate_subscriber('Tech Solutions', '9876543210', 'IT Services', '2010-03-15', '2023-01-01', '789 Pine Blvd, Suite 300, Business City', 'info@techsolutions.com', '5558765432','123456789');
SELECT insert_corporate_subscriber('Bright Future', '1134567890', 'Education', '2015-02-18', '2023-01-12', '456 Knowledge Rd, Suite 250, Raleigh', 'contact@brightfuture.com', '5559345678','123456789');
SELECT insert_corporate_subscriber('Next Horizon', '1234567890', 'Finance', '2018-08-30', '2023-01-13', '321 Wealth St, Suite 300, Columbus', 'info@nexthorizon.com', '5559456789','123456789');
SELECT insert_corporate_subscriber('Green Tech Solutions', '1534567890', 'Technology', '2017-09-05', '2023-01-16', '123 Innovation Lane, Suite 400, San Francisco', 'support@greentech.com', '5559789012','123456789');
SELECT insert_corporate_subscriber('Urban Living', '1634567890', 'Real Estate', '2014-04-10', '2023-01-17', '987 Skyline Ave, Suite 700, Seattle', 'contact@urbanliving.com', '5559890123','123456789');
SELECT insert_corporate_subscriber('Aqua World', '1734567890', 'Marine', '2019-01-22', '2023-01-18', '654 Ocean Blvd, Suite 200, Miami', 'info@aquaworld.com', '5559901234','123456789');
SELECT insert_corporate_subscriber('Visionary Ventures', '1834567890', 'Investment', '2012-11-15', '2023-01-19', '789 Growth Dr, Suite 800, Denver', 'hello@visionaryventures.com', '5559012345','123456789');
SELECT insert_corporate_subscriber('Solar Innovations', '1934567890', 'Renewable Energy', '2016-06-30', '2023-01-20', '321 Sunlight Way, Suite 500, Phoenix', 'support@solarinnovations.com', '5559123456','123456789');
SELECT insert_corporate_subscriber('Fresh Farms', '2034567890', 'Agriculture', '2013-03-18', '2023-01-21', '987 Harvest Rd, Suite 300, Nashville', 'info@freshfarms.com', '5559234567','123456789');
SELECT insert_corporate_subscriber('Safe Transport', '2134567890', 'Logistics', '2018-02-25', '2023-01-22', '123 Freight Ave, Suite 600, Dallas', 'contact@safetransport.com', '5559345678','123456789');

INSERT INTO energy (invoiceType, corporationPrice, individualPrice, carbonEmission)
VALUES ('Electricity', 2.07, 3.14, 0.4);

INSERT INTO energy (invoiceType, corporationPrice, individualPrice, carbonEmission)
VALUES ('Natural Gas', 7.37, 9.40, 2.1);

INSERT INTO energy (invoiceType, corporationPrice, individualPrice, carbonEmission)
VALUES ('Water', 15.68, 23.52, 0.3);


-- Bireysel abone için fatura ekleme (örnek)
SELECT insert_invoice(CURRENT_DATE, 100000001, 'Electricity', 300.5, 25.00);

-- Kurumsal abone için fatura ekleme (örnek)
SELECT insert_invoice(CURRENT_DATE, 100000002, 'Electricity', 1200.0, 150.00);

SELECT insert_individual_subscriber('John', 'Nice', '14434567891', '1990-04-18',
'2022-01-14', '789 Riven Rd, Apt 2B, Houston', 'j6hn.4nderson@houston.com', '5512345678','123456789');