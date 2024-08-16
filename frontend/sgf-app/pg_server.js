const { Pool } = require('pg');

const pool = new Pool({
  user: 'postgres',
  host: 'localhost',
  database: 'sgfication_data',
  password: 'gargar',
  port: 5432,
});

const saveSubmission = async (fileName, sgfData) => {
  const query = `
    INSERT INTO submissions (file_name, sgf_data)
    VALUES ($1, $2)
  `;
  await pool.query(query, [fileName, sgfData]);
};
