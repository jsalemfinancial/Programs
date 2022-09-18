/**
 * This file is loaded via the <script> tag in the index.html file and will
 * be executed in the renderer process for that window. No Node.js APIs are
 * available in this process because `nodeIntegration` is turned off and
 * `contextIsolation` is turned on. Use the contextBridge API in `preload.js`
 * to expose Node.js functionality from the main process.
 */

document.getElementById("submit-button").addEventListener("click", () => {
    window.formApi.fill({
        dealer: document.getElementsByName("dealer")[0].value,
        street: document.getElementsByName("street")[0].value,
        city: document.getElementsByName("city")[0].value,
        county: document.getElementsByName("county")[0].value,
        zip: document.getElementsByName("zip")[0].value,
        phone: document.getElementsByName("phone")[0].value,
        licenseNum: document.getElementsByName("licenseNum")[0].value,
        taxNum: document.getElementsByName("taxNum")[0].value,
        plateNum: document.getElementsByName("plateNum")[0].value,
        year: document.getElementsByName("year")[0].value,
        make: document.getElementsByName("make")[0].value,
        bodyStyle: document.getElementsByName("bodyStyle")[0].value,
        plateExpMonth: document.getElementsByName("plateExpMonth")[0].value,
        plateExpDay: document.getElementsByName("plateExpDay")[0].value,
        plateExpYear: document.getElementsByName("plateExpYear")[0].value,
        countyOfRes: document.getElementsByName("countyOfRes")[0].value,
        vin: document.getElementsByName("vin")[0].value,
        msrp: document.getElementsByName("msrp")[0].value,
        plateFee: document.getElementsByName("plateFee")[0].value,
        plateTransFee: document.getElementsByName("plateTransFee")[0].value,
        titleFee: document.getElementsByName("titleFee")[0].value,
        titleLateFee: document.getElementsByName("titleLateFee")[0].value,
        salesTax: document.getElementsByName("salesTax")[0].value,
        otherTax: document.getElementsByName("otherTax")[0].value,
        nonTax: document.getElementsByName("nonTax")[0].value,
        totalDelivered: document.getElementsByName("totalDelivered")[0].value,
        elecFilFee: document.getElementsByName("elecFilFee")[0].checked
    });
    console.log("Done!");
});

document.getElementsByTagName("body")[0].addEventListener("click", () => {
    console.log(document.getElementsByName("elecFilFee")[0].checked);
});