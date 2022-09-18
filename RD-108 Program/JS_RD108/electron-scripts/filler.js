const {PDFDocument} = require("pdf-lib");
const {writeFileSync, readFileSync} = require("fs");

module.exports = async function fillFields(data) {
  let dataDict = {};
  Object.assign(dataDict, data);

  const FORM_DOC = await PDFDocument.load(readFileSync("../RD-108/RD-108_MI.pdf"));
  var form = FORM_DOC.getForm();

  // var fields = form.getFields();

  // fields.forEach((field) => {
  //   var type = field.constructor.name;
  //   var name = field.getName();
    
  //   console.log(`${type}: ${name}`);
  // });

  const VEHICLE_DEALER = form.getTextField("Vehicle Dealer");
  VEHICLE_DEALER.setFontSize(12);
  VEHICLE_DEALER.setText(dataDict["dealer"]);

  const DEALER_STREET_ADDRESS = form.getTextField("Dealer Street Address");
  DEALER_STREET_ADDRESS.setFontSize(12);
  DEALER_STREET_ADDRESS.setText(dataDict["street"]);

  const DEALER_CITY = form.getTextField("Dealer City");
  DEALER_CITY.setFontSize(12);
  DEALER_CITY.setText(dataDict["city"]);

  const DEALER_COUNTY = form.getTextField("Dealer County");
  DEALER_COUNTY.setFontSize(10);
  DEALER_COUNTY.setText(dataDict["county"]);

  const DEALER_ZIP = form.getTextField("Dealer Zip Code");
  DEALER_ZIP.setFontSize(10);
  DEALER_ZIP.setText(dataDict["zip"]);

  const DEALER_PHONE = form.getTextField("Dealer Phone Number");
  DEALER_PHONE.setFontSize(10);
  DEALER_PHONE.setText(dataDict["phone"]);

  const DEALER_SALES_TAX_NUM = form.getTextField("Sales Tax License Number");
  DEALER_SALES_TAX_NUM.setFontSize(10);
  DEALER_SALES_TAX_NUM.setText(dataDict["taxNum"]);

  const DEALER_LICENSE_NUM = form.getTextField("Dealer License Number");
  DEALER_LICENSE_NUM.setFontSize(10);
  DEALER_LICENSE_NUM.setText(dataDict["licenseNum"]);

  const PLATE_NUM = form.getTextField("Plate Number");
  PLATE_NUM.setFontSize(10);
  PLATE_NUM.setText(dataDict["plateNum"]);

  const YEAR = form.getTextField("Vehicle Year");
  YEAR.setFontSize(10);
  YEAR.setText(dataDict["year"]);

  const MAKE = form.getTextField("Make");
  MAKE.setFontSize(10);
  MAKE.setText(dataDict["make"]);

  const BODY_STYLE = form.getTextField("Body Style");
  BODY_STYLE.setFontSize(10);
  BODY_STYLE.setText(dataDict["bodyStyle"]);

  const PLATE_EXP_MONTH = form.getTextField("Month");
  PLATE_EXP_MONTH.setFontSize(10);
  PLATE_EXP_MONTH.setText(dataDict["plateExpMonth"]);

  const PLATE_EXP_DAY = form.getTextField("Day");
  PLATE_EXP_DAY.setFontSize(10);
  PLATE_EXP_DAY.setText(dataDict["plateExpDay"]);

  const PLATE_EXP_YEAR = form.getTextField("Year");
  PLATE_EXP_YEAR.setFontSize(10);
  PLATE_EXP_YEAR.setText(dataDict["plateExpYear"]);

  const COUNTY_OF_RES = form.getTextField("County of Residence");
  COUNTY_OF_RES.setFontSize(10);
  COUNTY_OF_RES.setText(dataDict["countyOfRes"]);

  const VIN = form.getTextField("Purchase VIN");
  VIN.setFontSize(10);
  VIN.setText(dataDict["vin"]);

  const MSRP = form.getTextField("Fee Category or Weight");
  MSRP.setFontSize(10);
  MSRP.setText(dataDict["msrp"]);

  // Fees and Pricing

  let salesTax = parseFloat(dataDict["salesTax"]);
  let elecFee = 0;

  if (dataDict["elecFilFee"] == true) {
    elecFee = 24;
    const ELEC_FIL_FEE = form.getTextField("C");
    ELEC_FIL_FEE.setFontSize(10);
    ELEC_FIL_FEE.setText("24");
  }

  let purchasePrice = (parseFloat(dataDict["totalDelivered"]) - parseFloat(dataDict["plateFee"]) - 
                  parseFloat(dataDict["plateTransFee"]) - parseFloat(dataDict["titleFee"]) - parseFloat(dataDict["titleLateFee"]) -
                  parseFloat(dataDict["nonTax"]))/(1 + salesTax) -
                  (parseFloat(dataDict["otherTax"]) + elecFee);

  const PLATE_FEE = form.getTextField("License Plate Fee");
  PLATE_FEE.setFontSize(10);
  PLATE_FEE.setText(dataDict["plateFee"]);

  const PLATE_TRANS_FEE = form.getTextField("Plate Transfer Fee");
  PLATE_TRANS_FEE.setFontSize(10);
  PLATE_TRANS_FEE.setText(dataDict["plateTransFee"]);

  const TITLE_FEE = form.getTextField("Title Fee");
  TITLE_FEE.setFontSize(10);
  TITLE_FEE.setText(dataDict["titleFee"]);

  const TITLE_LATE_FEE = form.getTextField("Title Late Fee");
  TITLE_LATE_FEE.setFontSize(10);
  TITLE_LATE_FEE.setText(dataDict["titleLateFee"]);

  const PURCHASE_PRICE = form.getTextField("A");
  PURCHASE_PRICE.setFontSize(10);
  PURCHASE_PRICE.setText(((purchasePrice).toFixed(2)).toString());

  const OTHER_TAX = form.getTextField("B");
  OTHER_TAX.setFontSize(10);
  OTHER_TAX.setText(dataDict["otherTax"]);

  const TOTAL_TAX = form.getTextField("E");
  TOTAL_TAX.setFontSize(10);
  TOTAL_TAX.setText(((purchasePrice + parseFloat(dataDict["otherTax"]) + elecFee).toFixed(2)).toString());

  const SALES_PLATE_TITLE = form.getTextField("F");
  SALES_PLATE_TITLE.setFontSize(10);
  SALES_PLATE_TITLE.setText(((salesTax*(purchasePrice + parseFloat(dataDict["otherTax"]) + elecFee) + 
                                        parseFloat(dataDict["plateFee"]) + parseFloat(dataDict["plateTransFee"]) +
                                        parseFloat(dataDict["titleFee"]) + parseFloat(dataDict["titleLateFee"])).toFixed(2)).toString());

  const NON_TAX = form.getTextField("G");
  NON_TAX.setFontSize(10);
  NON_TAX.setText(dataDict["nonTax"]);

  const TOTAL_DELIVERED = form.getTextField("H");
  TOTAL_DELIVERED.setFontSize(10);
  TOTAL_DELIVERED.setText(dataDict["totalDelivered"]);

  const SALES_TAX = form.getTextField("Sales Tax");
  SALES_TAX.setFontSize(10);
  SALES_TAX.setText(((salesTax*(purchasePrice + parseFloat(dataDict["otherTax"]) + elecFee)).toFixed(2)).toString());

  const TOTAL_LINE_5 = form.getTextField("Total  Transfer to Line 5");
  TOTAL_LINE_5.setFontSize(10);
  TOTAL_LINE_5.setText(((salesTax*(purchasePrice + parseFloat(dataDict["otherTax"]) + elecFee) + 
                                  parseFloat(dataDict["plateFee"]) + parseFloat(dataDict["plateTransFee"]) +
                                  parseFloat(dataDict["titleFee"]) + parseFloat(dataDict["titleLateFee"])).toFixed(2)).toString());

  writeFileSync("../../RD-108_MI.pdf", await FORM_DOC.save());

  console.log("fillFields(args...) done writing!")
}

