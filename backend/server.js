const express = require("express");
const cors = require("cors");
const connectDB = require("./config/db");
const examRoutes = require("./routes/examRoutes");

require("dotenv").config();
connectDB();

const app = express();
app.use(express.json());
app.use(cors());

app.use("/api/exams", examRoutes);
const PORT = process.env.PORT || 5000;
app.listen(PORT, () => console.log(`🚀 Server running on port ${PORT}`));


// PS D:\TestPlatform\backend> netstat -ano | findstr :5000
// >> 
//   TCP    0.0.0.0:5000           0.0.0.0:0              LISTENING       25512
//   TCP    [::]:5000              [::]:0                 LISTENING       25512
// PS D:\TestPlatform\backend> netstat -ano | findstr :5000
// taskkill /PID 23996 /F

// SUCCESS: The process with PID 25512 has been terminated.
// PS D:\TestPlatform\backend> npm start
