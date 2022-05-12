/*
 * ATTENTION: The "eval" devtool has been used (maybe by default in mode: "development").
 * This devtool is neither made for production nor for readable output files.
 * It uses "eval()" calls to create a separate source file in the browser devtools.
 * If you are trying to read the output file, select a different devtool (https://webpack.js.org/configuration/devtool/)
 * or disable the default devtool with "devtool: false".
 * If you are looking for production-ready output files, see mode: "production" (https://webpack.js.org/configuration/mode/).
 */
var SiteJS;
/******/ (() => { // webpackBootstrap
/******/ 	"use strict";
/******/ 	var __webpack_modules__ = ({

/***/ "./assets/javascript/api.js":
/*!**********************************!*\
  !*** ./assets/javascript/api.js ***!
  \**********************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

eval("__webpack_require__.r(__webpack_exports__);\n/* harmony export */ __webpack_require__.d(__webpack_exports__, {\n/* harmony export */   \"getAction\": () => (/* binding */ getAction),\n/* harmony export */   \"getApiClient\": () => (/* binding */ getApiClient),\n/* harmony export */   \"Api\": () => (/* binding */ Api)\n/* harmony export */ });\nfunction _createForOfIteratorHelper(o, allowArrayLike) { var it = typeof Symbol !== \"undefined\" && o[Symbol.iterator] || o[\"@@iterator\"]; if (!it) { if (Array.isArray(o) || (it = _unsupportedIterableToArray(o)) || allowArrayLike && o && typeof o.length === \"number\") { if (it) o = it; var i = 0; var F = function F() {}; return { s: F, n: function n() { if (i >= o.length) return { done: true }; return { done: false, value: o[i++] }; }, e: function e(_e) { throw _e; }, f: F }; } throw new TypeError(\"Invalid attempt to iterate non-iterable instance.\\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.\"); } var normalCompletion = true, didErr = false, err; return { s: function s() { it = it.call(o); }, n: function n() { var step = it.next(); normalCompletion = step.done; return step; }, e: function e(_e2) { didErr = true; err = _e2; }, f: function f() { try { if (!normalCompletion && it[\"return\"] != null) it[\"return\"](); } finally { if (didErr) throw err; } } }; }\n\nfunction _unsupportedIterableToArray(o, minLen) { if (!o) return; if (typeof o === \"string\") return _arrayLikeToArray(o, minLen); var n = Object.prototype.toString.call(o).slice(8, -1); if (n === \"Object\" && o.constructor) n = o.constructor.name; if (n === \"Map\" || n === \"Set\") return Array.from(o); if (n === \"Arguments\" || /^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(n)) return _arrayLikeToArray(o, minLen); }\n\nfunction _arrayLikeToArray(arr, len) { if (len == null || len > arr.length) len = arr.length; for (var i = 0, arr2 = new Array(len); i < len; i++) { arr2[i] = arr[i]; } return arr2; }\n\nfunction getAction(apiRoot, action) {\n  // DRF dynamically sets the apiRoot based on the common shared prefix, so we attempt\n  // to inspect window.schema for the action - first searching for the namespaced version,\n  // then trying the action directly\n  var namespacedAction = apiRoot.concat(action);\n\n  if (!window.schema) {\n    console.error(\"window.schema not found. Did you forget to load your schemajs?\");\n  } else if (pathExistsInObject(action, window.schema.content)) {\n    return action;\n  } else if (pathExistsInObject(namespacedAction, window.schema.content)) {\n    return namespacedAction;\n  } else {\n    // fall back to default, even though it may not be valid\n    console.error('action ' + namespacedAction + 'not found in API schema. Some functionality may not work.');\n  }\n\n  return apiRoot.concat(action);\n}\n\nfunction pathExistsInObject(path, schema) {\n  var currentSchema = schema;\n\n  var _iterator = _createForOfIteratorHelper(path),\n      _step;\n\n  try {\n    for (_iterator.s(); !(_step = _iterator.n()).done;) {\n      var pathPart = _step.value;\n\n      if (currentSchema) {\n        currentSchema = currentSchema[pathPart];\n      } else {\n        return false;\n      }\n    }\n  } catch (err) {\n    _iterator.e(err);\n  } finally {\n    _iterator.f();\n  }\n\n  return Boolean(currentSchema);\n}\n\nfunction getApiClient() {\n  // this method will only work if you have also done the prerequisite steps on the page\n  // more details here: https://www.django-rest-framework.org/topics/api-clients/#javascript-client-library\n  var auth = new coreapi.auth.SessionAuthentication({\n    csrfCookieName: 'csrftoken',\n    csrfHeaderName: 'X-CSRFToken'\n  });\n  return new coreapi.Client({\n    auth: auth\n  });\n}\nvar Api = {\n  getAction: getAction,\n  getApiClient: getApiClient\n};\n\n//# sourceURL=webpack://SiteJS.%5Bname%5D/./assets/javascript/api.js?");

/***/ }),

/***/ "./assets/javascript/pegasus/examples/charts.js":
/*!******************************************************!*\
  !*** ./assets/javascript/pegasus/examples/charts.js ***!
  \******************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

eval("__webpack_require__.r(__webpack_exports__);\n/* harmony export */ __webpack_require__.d(__webpack_exports__, {\n/* harmony export */   \"Charts\": () => (/* binding */ Charts)\n/* harmony export */ });\n/* harmony import */ var _const__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ./const */ \"./assets/javascript/pegasus/examples/const.js\");\n/* harmony import */ var _api__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ../../api */ \"./assets/javascript/api.js\");\n\n\n\n\n\nfunction renderChart(chartType, bindTo, data) {\n  c3.generate({\n    bindto: bindTo,\n    data: {\n      columns: data,\n      type: chartType\n    }\n  });\n}\n\nfunction getListEmployeesAction() {\n  return (0,_api__WEBPACK_IMPORTED_MODULE_1__.getAction)(_const__WEBPACK_IMPORTED_MODULE_0__.API_ROOT, [\"employee-data\", \"list\"]);\n}\n\nvar Charts = {\n  renderChart: renderChart,\n  getListEmployeesAction: getListEmployeesAction\n};\n\n//# sourceURL=webpack://SiteJS.%5Bname%5D/./assets/javascript/pegasus/examples/charts.js?");

/***/ }),

/***/ "./assets/javascript/pegasus/examples/const.js":
/*!*****************************************************!*\
  !*** ./assets/javascript/pegasus/examples/const.js ***!
  \*****************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

eval("__webpack_require__.r(__webpack_exports__);\n/* harmony export */ __webpack_require__.d(__webpack_exports__, {\n/* harmony export */   \"API_ROOT\": () => (/* binding */ API_ROOT)\n/* harmony export */ });\n// if your API lives at a different namespace you can add it here\n// e.g. API_ROOT = [\"myapp\", \"api\"];\nvar API_ROOT = [\"pegasus\", \"employees\", \"api\"];\n\n//# sourceURL=webpack://SiteJS.%5Bname%5D/./assets/javascript/pegasus/examples/const.js?");

/***/ }),

/***/ "./assets/javascript/pegasus/pegasus.js":
/*!**********************************************!*\
  !*** ./assets/javascript/pegasus/pegasus.js ***!
  \**********************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

eval("__webpack_require__.r(__webpack_exports__);\n/* harmony export */ __webpack_require__.d(__webpack_exports__, {\n/* harmony export */   \"Charts\": () => (/* reexport safe */ _examples_charts__WEBPACK_IMPORTED_MODULE_0__.Charts)\n/* harmony export */ });\n/* harmony import */ var _examples_charts__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ./examples/charts */ \"./assets/javascript/pegasus/examples/charts.js\");\n\n\n//# sourceURL=webpack://SiteJS.%5Bname%5D/./assets/javascript/pegasus/pegasus.js?");

/***/ })

/******/ 	});
/************************************************************************/
/******/ 	// The module cache
/******/ 	var __webpack_module_cache__ = {};
/******/ 	
/******/ 	// The require function
/******/ 	function __webpack_require__(moduleId) {
/******/ 		// Check if module is in cache
/******/ 		var cachedModule = __webpack_module_cache__[moduleId];
/******/ 		if (cachedModule !== undefined) {
/******/ 			return cachedModule.exports;
/******/ 		}
/******/ 		// Create a new module (and put it into the cache)
/******/ 		var module = __webpack_module_cache__[moduleId] = {
/******/ 			// no module.id needed
/******/ 			// no module.loaded needed
/******/ 			exports: {}
/******/ 		};
/******/ 	
/******/ 		// Execute the module function
/******/ 		__webpack_modules__[moduleId](module, module.exports, __webpack_require__);
/******/ 	
/******/ 		// Return the exports of the module
/******/ 		return module.exports;
/******/ 	}
/******/ 	
/************************************************************************/
/******/ 	/* webpack/runtime/define property getters */
/******/ 	(() => {
/******/ 		// define getter functions for harmony exports
/******/ 		__webpack_require__.d = (exports, definition) => {
/******/ 			for(var key in definition) {
/******/ 				if(__webpack_require__.o(definition, key) && !__webpack_require__.o(exports, key)) {
/******/ 					Object.defineProperty(exports, key, { enumerable: true, get: definition[key] });
/******/ 				}
/******/ 			}
/******/ 		};
/******/ 	})();
/******/ 	
/******/ 	/* webpack/runtime/hasOwnProperty shorthand */
/******/ 	(() => {
/******/ 		__webpack_require__.o = (obj, prop) => (Object.prototype.hasOwnProperty.call(obj, prop))
/******/ 	})();
/******/ 	
/******/ 	/* webpack/runtime/make namespace object */
/******/ 	(() => {
/******/ 		// define __esModule on exports
/******/ 		__webpack_require__.r = (exports) => {
/******/ 			if(typeof Symbol !== 'undefined' && Symbol.toStringTag) {
/******/ 				Object.defineProperty(exports, Symbol.toStringTag, { value: 'Module' });
/******/ 			}
/******/ 			Object.defineProperty(exports, '__esModule', { value: true });
/******/ 		};
/******/ 	})();
/******/ 	
/************************************************************************/
/******/ 	
/******/ 	// startup
/******/ 	// Load entry module and return exports
/******/ 	// This entry module can't be inlined because the eval devtool is used.
/******/ 	var __webpack_exports__ = __webpack_require__("./assets/javascript/pegasus/pegasus.js");
/******/ 	(SiteJS = typeof SiteJS === "undefined" ? {} : SiteJS).pegasus = __webpack_exports__;
/******/ 	
/******/ })()
;