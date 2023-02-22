const express = require("express");
const { spawn } = require("child_process");
const cors = require("cors");
const app = express();

app.use(cors());
app.use(express.json());

const PORT = process.env.PORT || 10000;

app.listen(PORT, () => {
  console.log(`Listening on ${PORT}`);
});

app.post("/cardSearch", async (req, res) => {
  const input = await req.body.searchTerm;

  const childPython = spawn("python3", ["main.py", input]);

  childPython.stderr.on("data", (data) => {
    console.error(`stderr: ${data}`);
  });

  childPython.stdout.on("data", (data) => {
    return res.status(200).send(data);
  });

  childPython.on("close", (code) => {
    console.log(`child process exited with code ${code}`);
  });
});
