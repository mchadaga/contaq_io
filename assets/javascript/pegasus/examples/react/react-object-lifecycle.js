'use strict';
import React from "react";
import ReactDOM from "react-dom";
import EmployeeApplication from "./App";
import {getApiClient} from "../../../api";


const domContainer = document.querySelector('#object-lifecycle-home');


domContainer ? ReactDOM.render(
  <EmployeeApplication client={getApiClient()} urlBase={urlBase}/>
  , domContainer) : null;
