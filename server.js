const express = require("express");
const { spawn } = require("child_process");
const cors = require("cors");
const app = express();

app.use(cors());
app.use(express.json());

const PORT = process.env.PORT || 8000;

app.listen(PORT, () => {
  console.log(`Listening on ${PORT}`);
});

app.get("/cardSearch", (req, res) => {
  console.log("Hello!");
});
app.post("/cardSearch", (req, res) => {
  const input = req.body.searchTerm;

  const childPython = spawn("python", ["web_scraping.py", input]);

  childPython.stdout.on("data", (data) => {
    console.log(`stdout: ${data}`);
    res.send(data);
  });

  childPython.stderr.on("data", (data) => {
    console.error(`stderr: ${data}`);
  });

  childPython.on("close", (code) => {
    console.log(`child process exited with code ${code}`);
  });
});
