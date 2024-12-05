//react
import React, { useEffect, useState } from "react";
import { useLocation, useParams } from "react-router-dom";
import { useNavigate } from "react-router-dom";

//components
import Graph from "../components/Graph";

//breadcrumb
import {
  Breadcrumb,
  BreadcrumbItem,
  BreadcrumbLink,
  BreadcrumbList,
  BreadcrumbPage,
  BreadcrumbSeparator,
} from "@/components/ui/breadcrumb";

//TODO: Grab Graph Data Here (frequency from News, Frequency from Social Media, Sentiment over Time)

const CryptoPage = () => {
  const { name } = useParams();
  const { state } = useLocation();

  const navigate = useNavigate();
  const handleButtonClick = () => {
    navigate(`/`);
  };

  let social_impressions = [];
  let social_source = {};
  let news_impressions = [];
  let news_source = {};

  for (const date in state.info) {
    let social_counter = 0;
    let news_counter = 0;
    for (const key in state.info[date]) {
      if (state.info[date][key].source_type === "social") {
        social_counter++;
        if (state.info[date][key].source_name in social_source) {
          social_source[state.info[date][key].source_name]++;
        } else {
          social_source[state.info[date][key].source_name] = 1;
        }
      } else {
        news_counter++;
        if (state.info[date][key].source_name in news_source) {
          news_source[state.info[date][key].source_name]++;
        } else {
          news_source[state.info[date][key].source_name] = 1;
        }
      }
    }

    let date_object = new Date(date);
    let epoch_date = date_object.getTime();

    social_impressions.push([epoch_date, social_counter]);
    news_impressions.push([epoch_date, news_counter]);
  }

  let avg_sent_scores = [];

  for (const date in state.info) {
    let sent_scores = [];
    for (const key in state.info[date]) {
      sent_scores.push(state.info[date][key].sentiment);
    }
    let avg_sent_score = sent_scores.reduce((a, b) => a + b) / sent_scores.length;

    let date_object = new Date(date);
    let epoch_date = date_object.getTime();

    avg_sent_scores.push([epoch_date, parseFloat(avg_sent_score.toFixed(2))]);
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
        name: "Impressions",
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
        name: "Impressions",
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
        name: "Avg Score",
        data: avg_sent_scores,
      },
    ],
    accessibility: {
      enabled: false,
    },
    yAxis: {
      title: {
        text: "Average Sentiment",
      },
      min: 0,
      max: 10,
      startOnTick: true,
    },
  };

  return (
    <>
      <div className="m-5">
        <Breadcrumb>
          <BreadcrumbList>
            <BreadcrumbItem>
              <BreadcrumbLink href="/">Home</BreadcrumbLink>
            </BreadcrumbItem>
            <BreadcrumbSeparator />
            <BreadcrumbItem>
              <BreadcrumbPage>{name}</BreadcrumbPage>
            </BreadcrumbItem>
          </BreadcrumbList>
        </Breadcrumb>

        <div className="flex justify-center items-center text-5xl mb-11">
          <div className="mr-5">
            <img style={{ height: 100, width: 100 }} src={`/${name}.svg`}></img>
          </div>
          <div>{name}</div>
        </div>

        <div className="grid grid-cols-7 mb-5">
          <div></div>
          <div className="text-lg text-center">
            Latest News Impression
            <br />
            <div className="text-4xl">{news_impressions.slice(-1)[0][1]}</div>
          </div>
          <div></div>
          <div className="text-lg text-center">
            Latest Average Sentiment
            <br />
            <div className="text-4xl">{state.latest_sent_score}</div>
          </div>
          <div></div>
          <div className="text-lg text-center">
            Latest Social Impression
            <br />
            <div className="text-4xl">{social_impressions.slice(-1)[0][1]}</div>
          </div>
          <div></div>
        </div>

        <div className="w-full grid grid-cols-8">
          <div></div>
          <div className="col-span-12">
            <div className="w-full grid grid-cols-12">
              <div></div>
              <div className="col-span-8">
                <Graph options={news} />
              </div>
              <div className="col-span-2 text-align mt-5 ">
                <ul>
                  {Object.entries(news_source).map(([key, value]) => (
                    <li key={key}>
                      {key}: {value}
                    </li>
                  ))}
                </ul>
              </div>
            </div>
          </div>
          <div></div>
          <div></div>
          <div className="col-span-12">
            <div className="w-full grid grid-cols-12">
              <div></div>
              <div className="col-span-8">
                <Graph options={social_media} />
              </div>
              <div className="col-span-2 text-align mt-5 font-sans">
                <ul>
                  {Object.entries(social_source).map(([key, value]) => (
                    <li key={key}>
                      {key}: {value}
                    </li>
                  ))}
                </ul>
              </div>
            </div>
          </div>
          <div></div>
          <div></div>
          <div className="col-span-12">
            <div className="w-full grid grid-cols-12">
              <div></div>
              <div className="col-span-8">
                <Graph options={sentiment} />
              </div>
              <div className="col-span-2 text-align mt-5">
                <ul>
                  {Object.entries({ ...social_source, ...news_source }).map(([key, value]) => (
                    <li key={key}>
                      {key}: {value}
                    </li>
                  ))}
                </ul>
              </div>
            </div>
          </div>
          <div></div>
        </div>
      </div>
    </>
  );
};

export default CryptoPage;
