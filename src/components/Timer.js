import React from "react";
import timewarp from "../timewarp";

class Timer extends React.Component {
  constructor(props) {
    super(props);
    this.state = { remaining: this.props.duration };
    this.parseTime = this.parseTime.bind(this);
    this.countdown = this.countdown.bind(this);
  }

  componentDidMount() {
    this.interval = setInterval(e => this.countdown(), timewarp.msInSeconds);
    this.countdown();
  }

  countdown() {
    const timeLeft = this.state.remaining;
    const nextPage = this.props.work ? "Finished" : "Next";
    if (this.state.remaining > 0) {
      this.setState({ remaining: timeLeft - 1 });
    } else {
      this.props.updateMachine(
        false,
        this.props.id,
        this.props.task,
        this.props.duration,
        nextPage
      );
      return;
    }
  }

  componentWillUnmount() {
    clearInterval(this.interval);
  }

  parseTime(sec) {
    // parses seconds into human friendly clock format
    let minutes = Math.floor(sec / 60);
    let seconds = sec % 60;
    if (seconds <= 0 && minutes <= 0) {
      return "00:00";
    }
    if (minutes < 10) minutes = `0${minutes}`;
    if (seconds < 10) seconds = `0${seconds}`;
    return `${minutes}:${seconds}`;
  }

  render() {
    let color;
    if (this.props.work) color = { color: "green" };
    else color = { color: "red" };
    const taskInfo = `Current task: ${this.props.task}`;
    const breakInfo = `Taking a break...`;
    return (
      <>
        <p className="clock" style={color} id="clockInfo">
          {this.props.work && taskInfo}
          {!this.props.work && breakInfo}
        </p>
        <p style={color} className="clock">
          {this.parseTime(this.state.remaining)} left
        </p>
      </>
    );
  }
}

export default Timer;
