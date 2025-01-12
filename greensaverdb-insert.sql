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


INSERT INTO energy (invoiceType, corporationPrice, individualPrice, carbonEmission)
VALUES ('Electricity', 2.07, 3.14, 0.4);

INSERT INTO energy (invoiceType, corporationPrice, individualPrice, carbonEmission)
VALUES ('Water', 1.56, 2.35, 0.3);

INSERT INTO energy (invoiceType, corporationPrice, individualPrice, carbonEmission)
VALUES ('Natural Gas', 7.37, 9.40, 2.1);

-- Bireysel aboneler için faturalar
SELECT insert_invoice('2023-01-20', 100000000, 'Electricity', 150.75, 473.355); -- 150.75 * 3.14
SELECT insert_invoice('2023-01-21', 100000001, 'Water', 80.50, 189.175); -- 80.50 * 2.35
SELECT insert_invoice('2023-01-22', 100000002, 'Natural Gas', 200.00, 1880.00); -- 200.00 * 9.40
SELECT insert_invoice('2023-01-23', 100000003, 'Electricity', 300.00, 942.00); -- 300.00 * 3.14
SELECT insert_invoice('2023-01-24', 100000004, 'Water', 90.20, 211.970); -- 90.20 * 2.35
SELECT insert_invoice('2023-01-25', 100000005, 'Natural Gas', 250.75, 2357.050); -- 250.75 * 9.40
SELECT insert_invoice('2023-01-26', 100000006, 'Electricity', 120.40, 378.056); -- 120.40 * 3.14
SELECT insert_invoice('2023-01-27', 100000007, 'Water', 65.80, 154.630); -- 65.80 * 2.35
SELECT insert_invoice('2023-01-28', 100000008, 'Natural Gas', 180.00, 1692.00); -- 180.00 * 9.40
SELECT insert_invoice('2023-01-29', 100000009, 'Electricity', 95.00, 298.30); -- 95.00 * 3.14
SELECT insert_invoice('2023-01-30', 100000000, 'Water', 100.25, 235.5875); -- 100.25 * 2.35
SELECT insert_invoice('2023-01-31', 100000001, 'Natural Gas', 150.50, 1414.70); -- 150.50 * 9.40
SELECT insert_invoice('2023-02-01', 100000002, 'Electricity', 175.75, 551.855); -- 175.75 * 3.14
SELECT insert_invoice('2023-02-02', 100000003, 'Water', 85.00, 199.75); -- 85.00 * 2.35
SELECT insert_invoice('2023-02-03', 100000004, 'Natural Gas', 300.30, 2822.82); -- 300.30 * 9.40
SELECT insert_invoice('2023-02-04', 100000005, 'Electricity', 110.50, 346.97); -- 110.50 * 3.14
SELECT insert_invoice('2023-02-05', 100000006, 'Water', 78.60, 184.71); -- 78.60 * 2.35
SELECT insert_invoice('2023-02-06', 100000007, 'Natural Gas', 220.00, 2068.00); -- 220.00 * 9.40
SELECT insert_invoice('2023-02-07', 100000008, 'Electricity', 140.00, 439.60); -- 140.00 * 3.14
SELECT insert_invoice('2023-02-08', 100000009, 'Water', 92.50, 217.375); -- 92.50 * 2.35
SELECT insert_invoice('2023-02-09', 100000000, 'Electricity', 180.50, 567.57); -- 180.50 * 3.14
SELECT insert_invoice('2023-03-10', 100000000, 'Electricity', 220.75, 692.57); -- 220.75 * 3.14
SELECT insert_invoice('2023-02-11', 100000000, 'Water', 120.00, 282.00); -- 120.00 * 2.35
SELECT insert_invoice('2023-04-12', 100000000, 'Water', 150.50, 353.68); -- 150.50 * 2.35
SELECT insert_invoice('2023-02-13', 100000000, 'Natural Gas', 200.75, 1880.05); -- 200.75 * 9.40
SELECT insert_invoice('2023-06-14', 100000000, 'Natural Gas', 250.00, 2350.00); -- 250.00 * 9.40
SELECT insert_invoice('2023-07-15', 100000000, 'Natural Gas', 100.25, 942.35); -- 100.25 * 9.40

-- Kurumsal aboneler için faturalar
SELECT insert_invoice('2023-01-20', 100000010, 'Electricity', 1000.00, 2070.00); -- 1000.00 * 2.07
SELECT insert_invoice('2023-01-21', 100000011, 'Water', 750.00, 1170.00); -- 750.00 * 1.56
SELECT insert_invoice('2023-01-22', 100000012, 'Natural Gas', 500.00, 3685.00); -- 500.00 * 7.37
SELECT insert_invoice('2023-01-23', 100000013, 'Electricity', 1200.00, 2484.00); -- 1200.00 * 2.07
SELECT insert_invoice('2023-01-24', 100000014, 'Water', 630.50, 983.580); -- 630.50 * 1.56
SELECT insert_invoice('2023-01-25', 100000015, 'Natural Gas', 800.00, 5896.00); -- 800.00 * 7.37
SELECT insert_invoice('2023-01-26', 100000016, 'Electricity', 950.00, 1966.50); -- 950.00 * 2.07
SELECT insert_invoice('2023-01-27', 100000017, 'Water', 420.00, 655.20); -- 420.00 * 1.56
SELECT insert_invoice('2023-01-28', 100000018, 'Natural Gas', 600.00, 4422.00); -- 600.00 * 7.37
SELECT insert_invoice('2023-01-29', 100000019, 'Electricity', 800.00, 1656.00); -- 800.00 * 2.07
SELECT insert_invoice('2023-01-30', 100000010, 'Water', 1200.00, 1872.00); -- 1200.00 * 1.56
SELECT insert_invoice('2023-01-31', 100000011, 'Natural Gas', 450.75, 3321.0275); -- 450.75 * 7.37
SELECT insert_invoice('2023-02-01', 100000012, 'Electricity', 1350.00, 2794.50); -- 1350.00 * 2.07
SELECT insert_invoice('2023-02-02', 100000013, 'Water', 800.50, 1240.78); -- 800.50 * 1.56
SELECT insert_invoice('2023-02-03', 100000014, 'Natural Gas', 950.00, 7001.50); -- 950.00 * 7.37
SELECT insert_invoice('2023-02-04', 100000015, 'Electricity', 880.00, 1821.60); -- 880.00 * 2.07
SELECT insert_invoice('2023-02-05', 100000016, 'Water', 610.00, 951.60); -- 610.00 * 1.56
SELECT insert_invoice('2023-02-06', 100000017, 'Natural Gas', 750.25, 5523.3425); -- 750.25 * 7.37
SELECT insert_invoice('2023-02-07', 100000018, 'Electricity', 900.00, 1863.00); -- 900.00 * 2.07
SELECT insert_invoice('2023-02-08', 100000019, 'Water', 490.00, 764.40); -- 490.00 * 1.56