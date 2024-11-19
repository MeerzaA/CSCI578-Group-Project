import React from "react";
import Highcharts from "highcharts/highstock";
import HighchartsReact from "highcharts-react-official";



const Graph = (props) => (
  <HighchartsReact
    highcharts={Highcharts}
    constructorType={"stockChart"}
    options={props.options}
  />
);

export default Graph;
