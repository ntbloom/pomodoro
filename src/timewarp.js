// speeds up time for faster development cycles

const production = false;
let timewarp;
if (production) {
  timewarp = {
    msInSeconds: 1000,
    duration: { work: 1500, break: 300 }
  };
} else {
  timewarp = {
    msInSeconds: 5,
    duration: { work: 300, break: 300 }
  };
}
export default timewarp;
