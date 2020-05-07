import React from "react";
import { url } from "../url";

class Results extends React.Component {
  constructor(props) {
    super(props);
    this.state = { ready: false };
    this.getAllTasks = this.getAllTasks.bind(this);
    this.handleClick = this.handleClick.bind(this);
  }
  handleClick() {
    this.props.updateMachine(
      this.props.work,
      this.props.id,
      this.props.task,
      this.props.duration,
      "Entries"
    );
  }

  getAllTasks() {
    fetch(`${url}/get-all-tasks`)
      .then(response => {
        return response.json();
      })
      .then(data => {
        this.setState({
          tasks: data,
          ready: true
        });
      });
  }

  componentDidMount() {
    this.getAllTasks();
  }

  render() {
    if (this.state.ready) {
      const tasksObj = this.state.tasks.tasks;
      const tasks = tasksObj.map(i => (
        <li
          type="triangle"
          key={i.id}
          style={i.done === 1 ? { color: "green" } : { color: "red" }}
        >
          <strong>{i.short}</strong> -- {i.desc}
        </li>
      ));
      return (
        <div id="results">
          <h1>Tasks you've worked on</h1>
          <ul>
            {Object.keys(tasksObj).length === 0
              ? "No tasks started yet..."
              : tasks}
          </ul>
          <button onClick={this.handleClick} className="clickButton">
            Start a new task
          </button>
        </div>
      );
    }
    return null;
  }
}

export default Results;
