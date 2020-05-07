import React from "react";
import { url } from "../url";
import crc32 from "crc/crc32";
import timewarp from "../timewarp";

class Entries extends React.Component {
  constructor(props) {
    super(props);
    this.state = {};
    this.handleSubmit = this.handleSubmit.bind(this);
    this.makeHash = this.makeHash.bind(this);
    this.seeResults = this.seeResults.bind(this);
  }

  makeHash(text) {
    // hash the name of the task to ensure unique taskid in the database
    return crc32(text).toString(16);
  }

  handleSubmit(e) {
    e.preventDefault();
    const data = new FormData(e.target);
    const short = data.get("short");
    const desc = data.get("desc");
    const id = this.makeHash(data.get("desc").concat(Date.now()));

    // prettier-ignore
    const payload = {
      "short": short,
      "desc": desc,
      "id": id,
      "done": 0
    };

    fetch(`${url}/add-task/`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify(payload)
    });
    this.props.updateMachine(
      true,
      id,
      short,
      timewarp.duration.work,
      "Timer"
    );
  }

  seeResults() {
    this.props.updateMachine(
      this.props.work,
      this.props.id,
      this.props.task,
      this.props.duration,
      "Results"
    );
  }

  render() {
    return (
      <div>
        <h1>Enter a task below to get started</h1>
        <form
          id="enterTaskWrapper"
          onSubmit={this.handleSubmit}
          method="post"
        >
          <div className="entryForm">
            <label>
              Short task name
              <span className="maxLength">max 50 characters</span>
            </label>
            <br />
            <input
              type="text"
              name="short"
              maxlength="50"
              size="45"
              placeholder="a quick description of the task"
              required
            />
          </div>
          <br />
          <br />
          <div className="entryForm">
            <label>
              Detailed Description{" "}
              <span className="maxLength">max 240 characters</span>
            </label>
            <br />
            <textarea
              name="desc"
              rows="5"
              cols="50"
              maxLength="240"
              placeholder="some more info about the task"
              wrap="soft"
              required
            />
          </div>
          <div className="entryForm">
            <input
              className="clickButton"
              id="enterTask"
              type="submit"
              value="Start this task"
            />
            <button
              onClick={this.seeResults}
              className="clickButton"
              id="seeResultsButton"
            >
              See what other tasks I've worked on
            </button>
          </div>
        </form>
      </div>
    );
  }
}

export default Entries;
