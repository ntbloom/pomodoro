/* 
A finite state machine to manage the state of the application.
The class renders child components using a switch statement and passes a 
callback function to each child to update state. The loop begins with an
"enter a task to get started" page and starts an infinite loop until the user 
closes the page.
*/

import React from "react";
import Timer from "./Timer";
import Results from "./Results";
import Entries from "./Entries";
import Finished from "./Finished";
import Next from "./Next";

class PomodoroMachine extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      childComponent: "Entries"
    };
    this.updateMachine = this.updateMachine.bind(this);
  }

  updateMachine(work, id, task, duration, childComponent) {
    // send data back upstream
    this.setState({
      work: work,
      id: id,
      task: task,
      duration: duration,
      childComponent: childComponent
    });
  }
  render() {
    const timer = (
      <Timer
        work={this.state.work}
        id={this.state.id}
        task={this.state.task}
        duration={this.state.duration}
        updateMachine={this.updateMachine}
      />
    );
    const finished = (
      <Finished
        work={this.state.work}
        id={this.state.id}
        task={this.state.task}
        duration={this.state.duration}
        updateMachine={this.updateMachine}
      />
    );
    const next = (
      <Next
        work={this.state.work}
        id={this.state.id}
        task={this.state.task}
        duration={this.state.duration}
        updateMachine={this.updateMachine}
      />
    );
    const results = <Results updateMachine={this.updateMachine} />;
    const entries = <Entries updateMachine={this.updateMachine} />;

    const childComponent = this.state.childComponent;
    switch (childComponent) {
      case "Timer":
        return timer;
      case "Results":
        return results;
      case "Entries":
        return entries;
      case "Finished":
        return finished;
      case "Next":
        return next;
      default:
        return "Entries";
    }
  }
}

export default PomodoroMachine;
