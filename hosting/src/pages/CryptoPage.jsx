//react
import React, { useEffect, useState } from "react";
import { useLocation, useParams } from "react-router-dom";
import { useNavigate } from "react-router-dom";

//components
import Graph from "../components/Graph";
import { Button } from "../components/ui/button";

//TODO: Grab Graph Data Here (frequency from News, Frequency from Social Media, Sentiment over Time)

const CryptoPage = () => {
  const { name } = useParams();
  const { state } = useLocation();

  const navigate = useNavigate();
  const handleButtonClick = () => {
    navigate(`/`);
  };

  console.log(state);


  let social_impressions = []
  let news_impressions = []

  for (const date in state.info) {
    let social_counter = 0
    let news_counter = 0
    for (const key in state.info[date]) {
      if (state.info[date][key].source_type === "social"){
        social_counter++
      }
      else {
        news_counter++
      }
    }

    let date_object = new Date(date)
    let epoch_date = date_object.getTime()

    social_impressions.push([epoch_date, social_counter])
    news_impressions.push([epoch_date, news_counter])
  }



  let avg_sent_scores = []

  for (const date in state.info) {
    let sent_scores = [];
    for (const key in state.info[date]) {
      sent_scores.push(state.info[date][key].sentiment);
    }
    let avg_sent_score = sent_scores.reduce((a, b) => a + b) / sent_scores.length;

    let date_object = new Date(date)
    let epoch_date = date_object.getTime()

    avg_sent_scores.push([epoch_date, parseFloat(avg_sent_score.toFixed(2))])
  }


  const news = {
    title: {
      text: "News Impressions",
    },
    accessibility: {
      enabled: false,
    },

    series: [
      {
        data: news_impressions,
      },
    ],
  };

  const social_media = {
    title: {
      text: "Social Media Impressions",
    },
    accessibility: {
      enabled: false,
    },
    series: [
      {
        data: social_impressions,
      },
    ],
  };

  const sentiment = {
    title: {
      text: "Sentiment",
    },
    series: [
      {
        data: avg_sent_scores,
      },
    ],
    accessibility: {
      enabled: false,
    },
    yAxis: {
      title: {
        text: 'Average Sentiment',
      },
      min: 0, 
      max: 10,
      startOnTick: true,
    }
  };

  return (
    <>
      <div className="m-5">
        <Button onClick={handleButtonClick}>Home</Button>
        <div className="text-center">{name}</div>
        <div className="w-full grid grid-cols-4">
          <div></div>
          <div className="col-span-6 md:col-span-2">
            <Graph options={news} />
          </div>
          <div></div>
          <div></div>
          <div className="col-span-6 md:col-span-2">
            <Graph options={social_media} />
          </div>
          <div></div>
          <div></div>
          <div className="col-span-6 md:col-span-2">
            <Graph options={sentiment} />
          </div>
          <div></div>
        </div>
      </div>
    </>
  );
};

export default CryptoPage;
