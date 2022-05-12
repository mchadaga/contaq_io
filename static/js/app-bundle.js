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
/******/ 	var __webpack_modules__ = ({

/***/ "./assets/javascript/api.js":
/*!**********************************!*\
  !*** ./assets/javascript/api.js ***!
  \**********************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
eval("__webpack_require__.r(__webpack_exports__);\n/* harmony export */ __webpack_require__.d(__webpack_exports__, {\n/* harmony export */   \"getAction\": () => (/* binding */ getAction),\n/* harmony export */   \"getApiClient\": () => (/* binding */ getApiClient),\n/* harmony export */   \"Api\": () => (/* binding */ Api)\n/* harmony export */ });\nfunction _createForOfIteratorHelper(o, allowArrayLike) { var it = typeof Symbol !== \"undefined\" && o[Symbol.iterator] || o[\"@@iterator\"]; if (!it) { if (Array.isArray(o) || (it = _unsupportedIterableToArray(o)) || allowArrayLike && o && typeof o.length === \"number\") { if (it) o = it; var i = 0; var F = function F() {}; return { s: F, n: function n() { if (i >= o.length) return { done: true }; return { done: false, value: o[i++] }; }, e: function e(_e) { throw _e; }, f: F }; } throw new TypeError(\"Invalid attempt to iterate non-iterable instance.\\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.\"); } var normalCompletion = true, didErr = false, err; return { s: function s() { it = it.call(o); }, n: function n() { var step = it.next(); normalCompletion = step.done; return step; }, e: function e(_e2) { didErr = true; err = _e2; }, f: function f() { try { if (!normalCompletion && it[\"return\"] != null) it[\"return\"](); } finally { if (didErr) throw err; } } }; }\n\nfunction _unsupportedIterableToArray(o, minLen) { if (!o) return; if (typeof o === \"string\") return _arrayLikeToArray(o, minLen); var n = Object.prototype.toString.call(o).slice(8, -1); if (n === \"Object\" && o.constructor) n = o.constructor.name; if (n === \"Map\" || n === \"Set\") return Array.from(o); if (n === \"Arguments\" || /^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(n)) return _arrayLikeToArray(o, minLen); }\n\nfunction _arrayLikeToArray(arr, len) { if (len == null || len > arr.length) len = arr.length; for (var i = 0, arr2 = new Array(len); i < len; i++) { arr2[i] = arr[i]; } return arr2; }\n\nfunction getAction(apiRoot, action) {\n  // DRF dynamically sets the apiRoot based on the common shared prefix, so we attempt\n  // to inspect window.schema for the action - first searching for the namespaced version,\n  // then trying the action directly\n  var namespacedAction = apiRoot.concat(action);\n\n  if (!window.schema) {\n    console.error(\"window.schema not found. Did you forget to load your schemajs?\");\n  } else if (pathExistsInObject(action, window.schema.content)) {\n    return action;\n  } else if (pathExistsInObject(namespacedAction, window.schema.content)) {\n    return namespacedAction;\n  } else {\n    // fall back to default, even though it may not be valid\n    console.error('action ' + namespacedAction + 'not found in API schema. Some functionality may not work.');\n  }\n\n  return apiRoot.concat(action);\n}\n\nfunction pathExistsInObject(path, schema) {\n  var currentSchema = schema;\n\n  var _iterator = _createForOfIteratorHelper(path),\n      _step;\n\n  try {\n    for (_iterator.s(); !(_step = _iterator.n()).done;) {\n      var pathPart = _step.value;\n\n      if (currentSchema) {\n        currentSchema = currentSchema[pathPart];\n      } else {\n        return false;\n      }\n    }\n  } catch (err) {\n    _iterator.e(err);\n  } finally {\n    _iterator.f();\n  }\n\n  return Boolean(currentSchema);\n}\n\nfunction getApiClient() {\n  // this method will only work if you have also done the prerequisite steps on the page\n  // more details here: https://www.django-rest-framework.org/topics/api-clients/#javascript-client-library\n  var auth = new coreapi.auth.SessionAuthentication({\n    csrfCookieName: 'csrftoken',\n    csrfHeaderName: 'X-CSRFToken'\n  });\n  return new coreapi.Client({\n    auth: auth\n  });\n}\nvar Api = {\n  getAction: getAction,\n  getApiClient: getApiClient\n};\n\n//# sourceURL=webpack://SiteJS.%5Bname%5D/./assets/javascript/api.js?");

/***/ }),

/***/ "./assets/javascript/app.js":
/*!**********************************!*\
  !*** ./assets/javascript/app.js ***!
  \**********************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
eval("__webpack_require__.r(__webpack_exports__);\n/* harmony export */ __webpack_require__.d(__webpack_exports__, {\n/* harmony export */   \"Payments\": () => (/* reexport safe */ _payments__WEBPACK_IMPORTED_MODULE_1__.Payments),\n/* harmony export */   \"Api\": () => (/* reexport safe */ _api__WEBPACK_IMPORTED_MODULE_2__.Api),\n/* harmony export */   \"Modals\": () => (/* reexport safe */ _web_modals__WEBPACK_IMPORTED_MODULE_3__.Modals),\n/* harmony export */   \"Cookies\": () => (/* binding */ Cookies)\n/* harmony export */ });\n/* harmony import */ var js_cookie__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! js-cookie */ \"./node_modules/js-cookie/src/js.cookie.js\");\n/* harmony import */ var js_cookie__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(js_cookie__WEBPACK_IMPORTED_MODULE_0__);\n/* harmony import */ var _payments__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ./payments */ \"./assets/javascript/payments.js\");\n/* harmony import */ var _api__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ./api */ \"./assets/javascript/api.js\");\n/* harmony import */ var _web_modals__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ./web/modals */ \"./assets/javascript/web/modals.js\");\n\n\n\n // pass-through for Cookies API\n\nvar Cookies = {\n  get: js_cookie__WEBPACK_IMPORTED_MODULE_0__.get,\n  set: js_cookie__WEBPACK_IMPORTED_MODULE_0__.set\n};\n\n//# sourceURL=webpack://SiteJS.%5Bname%5D/./assets/javascript/app.js?");

/***/ }),

/***/ "./assets/javascript/payments.js":
/*!***************************************!*\
  !*** ./assets/javascript/payments.js ***!
  \***************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
eval("__webpack_require__.r(__webpack_exports__);\n/* harmony export */ __webpack_require__.d(__webpack_exports__, {\n/* harmony export */   \"addInputToForm\": () => (/* binding */ addInputToForm),\n/* harmony export */   \"showOrClearError\": () => (/* binding */ showOrClearError),\n/* harmony export */   \"createCardElement\": () => (/* binding */ createCardElement),\n/* harmony export */   \"createPaymentIntent\": () => (/* binding */ createPaymentIntent),\n/* harmony export */   \"Payments\": () => (/* binding */ Payments)\n/* harmony export */ });\n/* harmony import */ var js_cookie__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! js-cookie */ \"./node_modules/js-cookie/src/js.cookie.js\");\n/* harmony import */ var js_cookie__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(js_cookie__WEBPACK_IMPORTED_MODULE_0__);\n\n\n\nfunction addInputToForm(form, name, value) {\n  var hiddenInput = document.createElement('input');\n  hiddenInput.setAttribute('type', 'hidden');\n  hiddenInput.setAttribute('name', name);\n  hiddenInput.setAttribute('value', value);\n  form.appendChild(hiddenInput);\n}\nfunction showOrClearError(errorMessage) {\n  var displayError = document.getElementById('card-errors');\n\n  if (errorMessage) {\n    displayError.textContent = errorMessage;\n  } else {\n    displayError.textContent = '';\n  }\n}\nfunction createCardElement(stripe) {\n  var elements = stripe.elements();\n  var classes = {\n    base: 'stripe-element',\n    focus: 'focused-stripe-element',\n    invalid: 'invalid-stripe-element',\n    complete: 'complete-stripe-element'\n  };\n  var style = {\n    base: {\n      fontSize: '16px'\n    }\n  }; // Create an instance of the card Element.\n\n  var cardElement = elements.create('card', {\n    classes: classes,\n    style: style\n  });\n  cardElement.mount(\"#card-element\");\n  cardElement.addEventListener('change', function (event) {\n    var errorMessage = event.error ? event.error.message : '';\n    showOrClearError(errorMessage);\n  });\n  return cardElement;\n}\nvar createPaymentIntent = function createPaymentIntent(createPaymentIntentUrl, paymentData) {\n  // creates a payment intent in stripe and populates the result in the passed in clientSecrets dictionary\n  // (potentially overwriting what was previous there, in the case of a coupon changing the price)\n  // returns a promise\n  return new Promise(function (resolve, reject) {\n    var csrfToken = js_cookie__WEBPACK_IMPORTED_MODULE_0___default().get('csrftoken');\n    paymentData = paymentData || {};\n    fetch(createPaymentIntentUrl, {\n      method: \"POST\",\n      headers: {\n        \"Content-Type\": \"application/json\",\n        'X-CSRFToken': csrfToken\n      },\n      credentials: 'same-origin',\n      body: JSON.stringify(paymentData)\n    }).then(function (result) {\n      return result.json();\n    }).then(function (data) {\n      resolve(data.client_secret);\n    })[\"catch\"](function (error) {\n      reject(error);\n    });\n  });\n};\nvar Payments = {\n  addInputToForm: addInputToForm,\n  createCardElement: createCardElement,\n  createPaymentIntent: createPaymentIntent,\n  showOrClearError: showOrClearError\n};\n\n//# sourceURL=webpack://SiteJS.%5Bname%5D/./assets/javascript/payments.js?");

/***/ }),

/***/ "./assets/javascript/web/modals.js":
/*!*****************************************!*\
  !*** ./assets/javascript/web/modals.js ***!
  \*****************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
eval("__webpack_require__.r(__webpack_exports__);\n/* harmony export */ __webpack_require__.d(__webpack_exports__, {\n/* harmony export */   \"initializeModal\": () => (/* binding */ initializeModal),\n/* harmony export */   \"Modals\": () => (/* binding */ Modals)\n/* harmony export */ });\nfunction initializeModal(modalId) {\n  var openSelector = arguments.length > 1 && arguments[1] !== undefined ? arguments[1] : '.modal-opener';\n  var closeSelector = arguments.length > 2 && arguments[2] !== undefined ? arguments[2] : '.modal-closer';\n  var modal = document.getElementById(modalId);\n  (document.querySelectorAll(openSelector) || []).forEach(function (modalOpener) {\n    modalOpener.addEventListener('click', function () {\n      modal.classList.add('is-active');\n    });\n  });\n  (document.querySelectorAll(closeSelector) || []).forEach(function (modalCloser) {\n    modalCloser.addEventListener('click', function () {\n      modal.classList.remove('is-active');\n    });\n  });\n}\nvar Modals = {\n  initializeModal: initializeModal\n};\n\n//# sourceURL=webpack://SiteJS.%5Bname%5D/./assets/javascript/web/modals.js?");

/***/ }),

/***/ "./node_modules/js-cookie/src/js.cookie.js":
/*!*************************************************!*\
  !*** ./node_modules/js-cookie/src/js.cookie.js ***!
  \*************************************************/
/***/ ((module, exports, __webpack_require__) => {

eval("var __WEBPACK_AMD_DEFINE_FACTORY__, __WEBPACK_AMD_DEFINE_RESULT__;/*!\n * JavaScript Cookie v2.2.1\n * https://github.com/js-cookie/js-cookie\n *\n * Copyright 2006, 2015 Klaus Hartl & Fagner Brack\n * Released under the MIT license\n */\n;(function (factory) {\n\tvar registeredInModuleLoader;\n\tif (true) {\n\t\t!(__WEBPACK_AMD_DEFINE_FACTORY__ = (factory),\n\t\t__WEBPACK_AMD_DEFINE_RESULT__ = (typeof __WEBPACK_AMD_DEFINE_FACTORY__ === 'function' ?\n\t\t(__WEBPACK_AMD_DEFINE_FACTORY__.call(exports, __webpack_require__, exports, module)) :\n\t\t__WEBPACK_AMD_DEFINE_FACTORY__),\n\t\t__WEBPACK_AMD_DEFINE_RESULT__ !== undefined && (module.exports = __WEBPACK_AMD_DEFINE_RESULT__));\n\t\tregisteredInModuleLoader = true;\n\t}\n\tif (true) {\n\t\tmodule.exports = factory();\n\t\tregisteredInModuleLoader = true;\n\t}\n\tif (!registeredInModuleLoader) {\n\t\tvar OldCookies = window.Cookies;\n\t\tvar api = window.Cookies = factory();\n\t\tapi.noConflict = function () {\n\t\t\twindow.Cookies = OldCookies;\n\t\t\treturn api;\n\t\t};\n\t}\n}(function () {\n\tfunction extend () {\n\t\tvar i = 0;\n\t\tvar result = {};\n\t\tfor (; i < arguments.length; i++) {\n\t\t\tvar attributes = arguments[ i ];\n\t\t\tfor (var key in attributes) {\n\t\t\t\tresult[key] = attributes[key];\n\t\t\t}\n\t\t}\n\t\treturn result;\n\t}\n\n\tfunction decode (s) {\n\t\treturn s.replace(/(%[0-9A-Z]{2})+/g, decodeURIComponent);\n\t}\n\n\tfunction init (converter) {\n\t\tfunction api() {}\n\n\t\tfunction set (key, value, attributes) {\n\t\t\tif (typeof document === 'undefined') {\n\t\t\t\treturn;\n\t\t\t}\n\n\t\t\tattributes = extend({\n\t\t\t\tpath: '/'\n\t\t\t}, api.defaults, attributes);\n\n\t\t\tif (typeof attributes.expires === 'number') {\n\t\t\t\tattributes.expires = new Date(new Date() * 1 + attributes.expires * 864e+5);\n\t\t\t}\n\n\t\t\t// We're using \"expires\" because \"max-age\" is not supported by IE\n\t\t\tattributes.expires = attributes.expires ? attributes.expires.toUTCString() : '';\n\n\t\t\ttry {\n\t\t\t\tvar result = JSON.stringify(value);\n\t\t\t\tif (/^[\\{\\[]/.test(result)) {\n\t\t\t\t\tvalue = result;\n\t\t\t\t}\n\t\t\t} catch (e) {}\n\n\t\t\tvalue = converter.write ?\n\t\t\t\tconverter.write(value, key) :\n\t\t\t\tencodeURIComponent(String(value))\n\t\t\t\t\t.replace(/%(23|24|26|2B|3A|3C|3E|3D|2F|3F|40|5B|5D|5E|60|7B|7D|7C)/g, decodeURIComponent);\n\n\t\t\tkey = encodeURIComponent(String(key))\n\t\t\t\t.replace(/%(23|24|26|2B|5E|60|7C)/g, decodeURIComponent)\n\t\t\t\t.replace(/[\\(\\)]/g, escape);\n\n\t\t\tvar stringifiedAttributes = '';\n\t\t\tfor (var attributeName in attributes) {\n\t\t\t\tif (!attributes[attributeName]) {\n\t\t\t\t\tcontinue;\n\t\t\t\t}\n\t\t\t\tstringifiedAttributes += '; ' + attributeName;\n\t\t\t\tif (attributes[attributeName] === true) {\n\t\t\t\t\tcontinue;\n\t\t\t\t}\n\n\t\t\t\t// Considers RFC 6265 section 5.2:\n\t\t\t\t// ...\n\t\t\t\t// 3.  If the remaining unparsed-attributes contains a %x3B (\";\")\n\t\t\t\t//     character:\n\t\t\t\t// Consume the characters of the unparsed-attributes up to,\n\t\t\t\t// not including, the first %x3B (\";\") character.\n\t\t\t\t// ...\n\t\t\t\tstringifiedAttributes += '=' + attributes[attributeName].split(';')[0];\n\t\t\t}\n\n\t\t\treturn (document.cookie = key + '=' + value + stringifiedAttributes);\n\t\t}\n\n\t\tfunction get (key, json) {\n\t\t\tif (typeof document === 'undefined') {\n\t\t\t\treturn;\n\t\t\t}\n\n\t\t\tvar jar = {};\n\t\t\t// To prevent the for loop in the first place assign an empty array\n\t\t\t// in case there are no cookies at all.\n\t\t\tvar cookies = document.cookie ? document.cookie.split('; ') : [];\n\t\t\tvar i = 0;\n\n\t\t\tfor (; i < cookies.length; i++) {\n\t\t\t\tvar parts = cookies[i].split('=');\n\t\t\t\tvar cookie = parts.slice(1).join('=');\n\n\t\t\t\tif (!json && cookie.charAt(0) === '\"') {\n\t\t\t\t\tcookie = cookie.slice(1, -1);\n\t\t\t\t}\n\n\t\t\t\ttry {\n\t\t\t\t\tvar name = decode(parts[0]);\n\t\t\t\t\tcookie = (converter.read || converter)(cookie, name) ||\n\t\t\t\t\t\tdecode(cookie);\n\n\t\t\t\t\tif (json) {\n\t\t\t\t\t\ttry {\n\t\t\t\t\t\t\tcookie = JSON.parse(cookie);\n\t\t\t\t\t\t} catch (e) {}\n\t\t\t\t\t}\n\n\t\t\t\t\tjar[name] = cookie;\n\n\t\t\t\t\tif (key === name) {\n\t\t\t\t\t\tbreak;\n\t\t\t\t\t}\n\t\t\t\t} catch (e) {}\n\t\t\t}\n\n\t\t\treturn key ? jar[key] : jar;\n\t\t}\n\n\t\tapi.set = set;\n\t\tapi.get = function (key) {\n\t\t\treturn get(key, false /* read as raw */);\n\t\t};\n\t\tapi.getJSON = function (key) {\n\t\t\treturn get(key, true /* read as json */);\n\t\t};\n\t\tapi.remove = function (key, attributes) {\n\t\t\tset(key, '', extend(attributes, {\n\t\t\t\texpires: -1\n\t\t\t}));\n\t\t};\n\n\t\tapi.defaults = {};\n\n\t\tapi.withConverter = init;\n\n\t\treturn api;\n\t}\n\n\treturn init(function () {});\n}));\n\n\n//# sourceURL=webpack://SiteJS.%5Bname%5D/./node_modules/js-cookie/src/js.cookie.js?");

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
/******/ 	/* webpack/runtime/compat get default export */
/******/ 	(() => {
/******/ 		// getDefaultExport function for compatibility with non-harmony modules
/******/ 		__webpack_require__.n = (module) => {
/******/ 			var getter = module && module.__esModule ?
/******/ 				() => (module['default']) :
/******/ 				() => (module);
/******/ 			__webpack_require__.d(getter, { a: getter });
/******/ 			return getter;
/******/ 		};
/******/ 	})();
/******/ 	
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
/******/ 	var __webpack_exports__ = __webpack_require__("./assets/javascript/app.js");
/******/ 	(SiteJS = typeof SiteJS === "undefined" ? {} : SiteJS).app = __webpack_exports__;
/******/ 	
/******/ })()
;