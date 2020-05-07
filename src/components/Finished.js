import React from "react";
import { url } from "../url";
import timewarp from "../timewarp";

class Finished extends React.Component {
  constructor(props) {
    super(props);
    this.state = {};
    this.clickYes = this.clickYes.bind(this);
    this.killComponent = this.killComponent.bind(this);
    this.completeTask = this.completeTask.bind(this);
  }

  killComponent() {
    const nextTaskIsWork = this.props.work ? true : false;
    this.props.updateMachine(
      nextTaskIsWork,
      this.props.id,
      this.props.task,
      timewarp.duration.break,
      "Timer"
    );
  }

  completeTask() {
    fetch(`${url}/finish-task/?taskid=${this.props.id}`, {
      method: "POST",
      headers: {
        "Content-Type": "text/plain"
      }
    });
  }

  async clickYes() {
    await this.completeTask();
    await this.killComponent();
  }

  render() {
    return (
      <div>
        <h1>
          Did you finish?
          <br />
          <br />
          task: <em>{this.props.task}</em>
        </h1>
        <div>
          <button
            onClick={this.clickYes}
            className="clickButton"
            id="yesButton"
          >
            Yes
          </button>
          <button
            className="clickButton"
            id="noButton"
            onClick={this.killComponent}
          >
            No
          </button>
        </div>
      </div>
    );
  }
}

export default Finished;
