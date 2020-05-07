import React from "react";
import { url } from "../url";

class Next extends React.Component {
  constructor(props) {
    super(props);
    this.state = {};
    this.seeResults = this.seeResults.bind(this);
    this.startNewTask = this.startNewTask.bind(this);
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
  startNewTask() {
    this.props.updateMachine(
      this.props.work,
      this.props.id,
      this.props.task,
      this.props.duration,
      "Entries"
    );
  }

  componentDidMount() {}

  render() {
    return (
      <div>
        <h1>What do you want to do next?</h1>
        <button
          onClick={this.startNewTask}
          className="clickButton"
          id="startNewTaskButton"
        >
          Start a new task
        </button>
        <button
          onClick={this.seeResults}
          className="clickButton"
          id="seeResultsButton"
        >
          See what other tasks I've worked on
        </button>
      </div>
    );
  }
}

export default Next;
