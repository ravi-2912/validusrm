import React from "react";
import { shallow } from "enzyme";
import renderer from "react-test-renderer";
import UsersList from "../components/UsersList";

const users = [
  {
    active: true,
    email: "ravi@gmail.com",
    id: 1,
    username: "ravi"
  },
  {
    active: true,
    email: "ravisingh@hotmail.com",
    id: 2,
    username: "ravisingh"
  }
];

test("UsersList renders properly", () => {
  const wrapper = shallow(<UsersList users={users} />);
  const element = wrapper.find("h4");
  expect(element.length).toBe(2);
  expect(element.get(0).props.children).toBe("ravi");
  expect(element.get(1).props.children).toBe("ravisingh");
});

test("UsersList renders a snapshot properly", () => {
  const tree = renderer.create(<UsersList users={users} />).toJSON();
  expect(tree).toMatchSnapshot();
});
