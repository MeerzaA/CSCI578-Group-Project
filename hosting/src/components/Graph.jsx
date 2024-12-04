import React from "react";
import Highcharts from "highcharts/highstock";
import HighchartsReact from "highcharts-react-official";

const Graph = (props) => (
  <>
    <div
      // style={{ width: "1200px", height: "500px" }}
      className="m-5 border border-indigo-500"
    >
      <HighchartsReact
        highcharts={Highcharts}
        containerProps={{ style: { height: "100%", width: "100%" } }}
        constructorType={"stockChart"}
        options={props.options}
      />
    </div>
  </>
);

export default Graph;
