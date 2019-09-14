import React from "react";
import { shallow } from "enzyme";
import App from "../App";

describe("Test that App renders properly", () => {
  it("renders without crashing", () => {
    shallow(<App />);
  });
});
