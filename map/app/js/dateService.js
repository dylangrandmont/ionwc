"use strict";

function DateService() {
}

DateService.prototype.getFormatDate = function(date) {
    const day = ('0' + date.getDate()).slice(-2);
    const month = ('0' + (date.getMonth() + 1)).slice(-2); //January is 0!
    const year = date.getFullYear();

    return year + "." + month + "." + day;
};

module.exports = DateService;

