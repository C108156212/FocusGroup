import React, { Component } from "react";

class page01 extends Component {
  constructor(props) {
    super(props);
    this.state = {
      posts: [],
    };
  }
  componentDidMount() {
    const url = "https://jsonplaceholder.typicode.com/albums/1/photos";
    fetch(url)
      .then((response) => response.json())
      .then((json) => this.setState({ posts: json }));
  }
  render() {
    return <p>Hello world!</p>;
  }
}

export default page01;
