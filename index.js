require('dotenv').config();
require("express-async-errors");



const express = require("express");
const app = express();

const connectDB = require("./db/connect");


// Middleware uses


app.use(express.json());

// Basic route
app.use("/", (req, res) => {
  res.json({
    "message": "Welcome to the Express API",
    "timestamp": new Date().toISOString()
  });
});

// Not Found Middleware
const notFound = require("./middleware/not-found");
app.use(notFound);

// Error Handler Middleware
const errorHandler = require("./middleware/error-handler");
app.use(errorHandler);

const port = process.env.PORT || 5000;

const start = async () => {
  try {
    await connectDB(process.env.MONGO_URL);
    app.listen(port, () => {
      console.log(`Server is listening on port ${port}...`);
      console.log(`Environment: ${process.env.NODE_ENV || 'development'}`);
    });
  } catch (error) {
    console.error("Failed to start server:", error);
    process.exit(1);
  }
};

start();
