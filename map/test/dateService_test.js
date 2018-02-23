describe("DateService", function() {
  var dateService;

  beforeEach(function() {
    dateService = new DateService();
  });

  it("should reformat date with years, months, and day", function() {
    var date = new Date();
    date.setFullYear(2020, 0, 14);
    var reformatedDate = dateService.getReformatedDate(date);
    expect(reformatedDate).toEqual("2020.01.14");
  });

});
