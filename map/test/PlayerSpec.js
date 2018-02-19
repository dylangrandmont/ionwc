describe("Player", function() {
  var DateService = require('../app/js/dateService');
  var dateService;

  beforeEach(function() {
    dateService = new DateService();
  });

  it("should reformat dates", function() {
    var date = new Date();
    date.setFullYear(2020, 0, 14);
    var reformatedDate = dateService.getFormatDate(date);
    expect(reformatedDate).toEqual("2020.01.14");
  });

});
