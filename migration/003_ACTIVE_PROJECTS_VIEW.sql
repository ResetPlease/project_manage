CREATE VIEW ActiveProjects AS
SELECT id, name, start_date
FROM Projects
WHERE end_date IS NULL;
