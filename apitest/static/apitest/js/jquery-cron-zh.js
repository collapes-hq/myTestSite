/*
 * jQuery gentleSelect plugin
 * http://shawnchin.github.com/jquery-cron
 *
 * Copyright (c) 2010 Shawn Chin.
 * Dual licensed under the MIT or GPL Version 2 licenses.
 *
 * Requires:
 * - jQuery
 * - jQuery gentleSelect plugin
 *
 * Usage:
 *  (JS)
 *
 *  // initialise like this
 *  var c = $('#cron').cron({
 *    initial: '9 10 * * *', # Initial value. default = "* * * * *"
 *    url_set: '/set/', # POST expecting {"cron": "12 10 * * 6"}
 *  });
 *
 *  // you can update values later
 *  c.cron("value", "1 2 3 4 *");
 *
 * // you can also get the current value using the "value" option
 * alert(c.cron("value"));
 *
 *  (HTML)
 *  <div id='cron'></div>
 *
 * Notes:
 * At this stage, we only support a subset of possible cron options.
 * For example, each cron entry can only be digits or "*", no commas
 * to denote multiple entries. We also limit the allowed combinations:
 * - Every minute : * * * * *
 * - Every hour   : ? * * * *
 * - Every day    : ? ? * * *
 * - Every week   : ? ? * * ?
 * - Every month  : ? ? ? * *
 * - Every year   : ? ? ? ? *
 */
(function($) {
    var defaults = {
        initial: "* * * * *",
        everyNmins: {
            minWidth: 100, // only applies if columns and itemWidth not set
            itemWidth: 30,
            columns: 4,
            rows: undefined,
            title: "时间单位: 分钟"
        },
        minuteOpts: {
            minWidth: 100, // only applies if columns and itemWidth not set
            itemWidth: 30,
            columns: 4,
            rows: undefined,
            title: "时间单位: 分钟"
        },
        timeHourOpts: {
            minWidth: 100, // only applies if columns and itemWidth not set
            itemWidth: 20,
            columns: 2,
            rows: undefined,
            title: "时间单位: 小时"
        },
        domOpts: {
            minWidth: 100, // only applies if columns and itemWidth not set
            itemWidth: 30,
            columns: undefined,
            rows: 10,
            title: "时间单位: 日期"
        },
        monthOpts: {
            minWidth: 100, // only applies if columns and itemWidth not set
            itemWidth: 100,
            columns: 2,
            rows: undefined,
            title: undefined
        },
        dowOpts: {
            minWidth: 100, // only applies if columns and itemWidth not set
            itemWidth: undefined,
            columns: undefined,
            rows: undefined,
            title: undefined
        },
        timeMinuteOpts: {
            minWidth: 100, // only applies if columns and itemWidth not set
            itemWidth: 20,
            columns: 4,
            rows: undefined,
            title: "时间单位: 分钟"
        },
        effectOpts: {
            openSpeed: 400,
            closeSpeed: 400,
            openEffect: "slide",
            closeEffect: "slide",
            hideOnMouseOut: true
        },
        url_set: undefined,
        customValues: undefined,
        onChange: undefined // callback function each time value changes
    };

    // -------  build some static data -------

    // options for minutes in an hour
    var str_opt_mih = "";
    for (var i = 0; i < 60; i++) {
        var j = (i < 10) ? "0" : "";
        str_opt_mih += "<option value='" + i + "'>" + j + i + "</option>\n";
    }

    // options for hours in a day
    var str_opt_hid = "";
    for (var i = 0; i < 24; i++) {
        var j = (i < 10) ? "0" : "";
        str_opt_hid += "<option value='" + i + "'>" + j + i + "</option>\n";
    }

    //options for Every N minutes
    var str_opt_enm = "";
    for (var i = 0; i < 60; i++) {
        var j = (i < 10) ? "0" : "";
        str_opt_enm += "<option value='" + "*/" + i + "'>" + j + i + "</option>\n";
    }

    // options for days of month
    var str_opt_dom = "";
    for (var i = 1; i < 32; i++) {
        if (i == 1 || i == 21) { var suffix = "st"; } else if (i == 2 || i == 22) { var suffix = "nd"; } else if (i == 3 || i == 23) { var suffix = "rd"; } else { var suffix = "th"; }
        str_opt_dom += "<option value='" + i + "'>" + (i > 9 ? i : ('0' + i)) + suffix + "</option>\n";
    }

    // options for months
    var str_opt_month = "";
    var months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"];
    var monthsZH = ["01月", "02月", "03月", "04月", "05月", "06月", "07月", "08月", "09月", "10月", "11月", "12月"];
    for (var i = 0; i < months.length; i++) { str_opt_month += "<option value='" + (i + 1) + "'>" + monthsZH[i] + "</option>\n"; }

    // options for day of week
    var str_opt_dow = "";
    var days = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"];
    var daysZH = ["周日", "周一", "周二", "周三", "周四", "周五", "周六"];
    for (var i = 0; i < days.length; i++) {
        str_opt_dow += "<option value='" + i + "'>" + daysZH[i] + "</option>\n";
    }

    // options for period
    var str_opt_period = "";
    var periods = ["everyNmins", "minute", "hour", "day", "week", "month", "year"];
    var periodsZH = ["每间隔几分钟", "每分钟", "每小时", "每天", "每周", "每月", "每年"];
    for (var i = 0; i < periods.length; i++) { str_opt_period += "<option value='" + periods[i] + "'>" + periodsZH[i] + "</option>\n"; }

    // display matrix
    var toDisplay = {
        "minute": [],
        "everyNmins": ["everyNmins"],
        "hour": ["mins"],
        "day": ["time"],
        "week": ["dow", "time"],
        "month": ["dom", "time"],
        "year": ["dom", "month", "time"]
    };

    var combinations = {
        "everyNmins": /^\*\/\d{1,2}\s(\*\s){3}\*$/, // "*/? * * * *"
        "minute": /^(\*\s){4}\*$/, // "* * * * *"
        "hour": /^\d{1,2}\s(\*\s){3}\*$/, // "? * * * *"
        "day": /^(\d{1,2}\s){2}(\*\s){2}\*$/, // "? ? * * *"
        "week": /^(\d{1,2}\s){2}(\*\s){2}\d{1,2}$/, // "? ? * * ?"
        "month": /^(\d{1,2}\s){3}\*\s\*$/, // "? ? ? * *"
        "year": /^(\d{1,2}\s){4}\*$/ // "? ? ? ? *"
    };

    // ------------------ internal functions ---------------
    function defined(obj) {
        if (typeof obj == "undefined") { return false; } else { return true; }
    }

    function undefinedOrObject(obj) { return (!defined(obj) || typeof obj == "object") }

    function getCronType(cron_str) {
        // check format of initial cron value
        var valid_cron = /^((\d{1,2}|\*|\*\/\d{1,2})\s){4}(\d{1,2}|\*)$/
        if (typeof cron_str != "string" || !valid_cron.test(cron_str)) {
            $.error("cron: invalid initial value");
            return undefined;
        }
        var d = cron_str.split(" ");
        var minval = [0, 0, 1, 1, 0];
        var maxval = [59, 23, 31, 12, 6];

        for (var i = 0; i < d.length; i++) {
            if (d[i] == "*")
                continue;
            else if (d[i].substring(0, 2) == "*/")
                var v = parseInt(d[i].replace(d[i].substring(0, 2), ''))
            else
                var v = parseInt(d[i]);

            if (defined(v) && v <= maxval[i] && v >= minval[i])
                continue;

            if (d[i].indexOf("/"))
                continue;
            $.error("cron: invalid value found (col " + (i + 1) + ") in " + o.initial);
            return undefined;
        }

        // determine combination
        for (var t in combinations) { if (combinations[t].test(cron_str)) { return t; } }

        // unknown combination
        $.error("cron: valid but unsupported cron format. sorry.");
        return undefined;
    }

    function hasError(c, o) {
        if (!defined(getCronType(o.initial))) { return true; }
        if (!undefinedOrObject(o.customValues)) { return true; }
        return false;
    }

    function getCurrentValue(c) {
        var b = c.data("block");
        var min = hour = day = month = dow = "*";
        var selectedPeriod = b["period"].find("select").val();
        switch (selectedPeriod) {
            case "everyNmins":
                min = b["everyNmins"].find("select").val();
                break;
            case "minute":
                break;
            case "hour":
                min = b["mins"].find("select").val();
                break;
            case "day":
                min = b["time"].find("select.crontimemin").val();
                hour = b["time"].find("select.crontimehour").val();
                break;
            case "week":
                min = b["time"].find("select.crontimemin").val();
                hour = b["time"].find("select.crontimehour").val();
                dow = b["dow"].find("select").val();
                break;
            case "month":
                min = b["time"].find("select.crontimemin").val();
                hour = b["time"].find("select.crontimehour").val();
                day = b["dom"].find("select").val();
                break;
            case "year":
                min = b["time"].find("select.crontimemin").val();
                hour = b["time"].find("select.crontimehour").val();
                day = b["dom"].find("select").val();
                month = b["month"].find("select").val();
                break;
            default:
                // we assume this only happens when customValues is set
                return selectedPeriod;
        }
        return [min, hour, day, month, dow].join(" ");
    }

    // -------------------  PUBLIC METHODS -----------------

    var methods = {
        init: function(opts) {
            // init options
            var options = opts ? opts : {}; /* default to empty obj */
            var o = $.extend([], defaults, options);
            var eo = $.extend({}, defaults.effectOpts, options.effectOpts);
            $.extend(o, {
                everyNmins: $.extend({}, defaults.everyNmins, eo, options.everyNmins),
                minuteOpts: $.extend({}, defaults.minuteOpts, eo, options.minuteOpts),
                domOpts: $.extend({}, defaults.domOpts, eo, options.domOpts),
                monthOpts: $.extend({}, defaults.monthOpts, eo, options.monthOpts),
                dowOpts: $.extend({}, defaults.dowOpts, eo, options.dowOpts),
                timeHourOpts: $.extend({}, defaults.timeHourOpts, eo, options.timeHourOpts),
                timeMinuteOpts: $.extend({}, defaults.timeMinuteOpts, eo, options.timeMinuteOpts)
            });

            // error checking
            if (hasError(this, o)) { return this; }

            // ---- define select boxes in the right order -----
            var block = [],
                custom_periods = "",
                cv = o.customValues;
            if (defined(cv)) { for (var key in cv) { custom_periods += "<option value='" + cv[key] + "'>" + key + "</option>\n"; } }
            block["period"] = $("<span class='cronperiod'>" +
                    "维度选择 <select name='cronperiod'>" + custom_periods +
                    str_opt_period + "</select> </span>")
                .appendTo(this)
                .data("root", this)
                .find("select")
                .bind("change.cron", event_handlers.periodChanged)
                .data("root", this)
                .gentleSelect(eo)
                .end();

            block["dom"] = $("<span class='cron-block cron-block-dom'>" +
                    " 的 <select name='crondom'>" + str_opt_dom +
                    "</select> </span>")
                .appendTo(this)
                .data("root", this)
                .find("select")
                .gentleSelect(o.domOpts)
                .data("root", this)
                .end();

            block["month"] = $("<span class='cron-block cron-block-month'>" +
                    " / <select name='cronmonth'>" + str_opt_month +
                    "</select </span>")
                .appendTo(this)
                .data("root", this)
                .find("select")
                .gentleSelect(o.monthOpts)
                .data("root", this)
                .end();

            block["mins"] = $("<span class='cron-block cron-block-mins'>" +
                    " 每小时的 <select name='cronmins'>" + str_opt_mih +
                    "</select> 分运行一次任务 </span>")
                .appendTo(this)
                .data("root", this)
                .find("select")
                .gentleSelect(o.minuteOpts)
                .data("root", this)
                .end();

            block["everyNmins"] = $("<span class='cron-block cron-block-everyNmins'>" +
                    " 每间隔 <select name='cronNmins'>" + str_opt_enm +
                    "</select> 分钟运行一次任务 </span>")
                .appendTo(this)
                .data("root", this)
                .find("select")
                .gentleSelect(o.everyNmins)
                .data("root", this)
                .end();

            block["dow"] = $("<span class='cron-block cron-block-dow'>" +
                    " 的 <select name='crondow'>" + str_opt_dow +
                    "</select> </span>")
                .appendTo(this)
                .data("root", this)
                .find("select")
                .gentleSelect(o.dowOpts)
                .data("root", this)
                .end();

            block["time"] = $("<span class='cron-block cron-block-time'>" +
                    " 的 <select name='crontimehour' class='crontimehour'>" + str_opt_hid +
                    "</select> 时 : <select name='crontimemin' class='crontimemin'>" + str_opt_mih +
                    "</select> 分运行一次任务 </span>")
                .appendTo(this)
                .data("root", this)
                .find("select.crontimehour")
                .gentleSelect(o.timeHourOpts)
                .data("root", this)
                .end()
                .find("select.crontimemin")
                .gentleSelect(o.timeMinuteOpts)
                .data("root", this)
                .end();

            block["controls"] = $("<span class='cron-controls'>&laquo; save " +
                    "<span class='cron-button cron-button-save'></span>" +
                    " </span>")
                .appendTo(this)
                .data("root", this)
                .find("span.cron-button-save")
                .bind("click.cron", event_handlers.saveClicked)
                .data("root", this)
                .end();

            this.find("select").bind("change.cron-callback", event_handlers.somethingChanged);
            this.data("options", o).data("block", block); // store options and block pointer
            this.data("current_value", o.initial); // remember base value to detect changes
            return methods["value"].call(this, o.initial); // set initial value
        },

        value: function(cron_str) {
            // when no args, act as getter
            if (!cron_str) { return getCurrentValue(this); }

            var t = getCronType(cron_str);
            if (!defined(t)) { alert("undefined t"); return false; }

            var block = this.data("block");
            var d;
            var v;

            d = cron_str.split(" ");
            v = {
                "mins": d[0],
                "hour": d[1],
                "dom": d[2],
                "month": d[3],
                "dow": d[4]
            };

            // update appropriate select boxes
            var targets = toDisplay[t];

            for (var i = 0; i < targets.length; i++) {
                var tgt = targets[i];
                if (tgt == "time") {
                    block[tgt]
                        .find("select.crontimehour")
                        .val(v["hour"]).gentleSelect("update")
                        .end()
                        .find("select.crontimemin")
                        .val(v["mins"]).gentleSelect("update")
                        .end();
                } else if (tgt == "everyNmins") {
                    block[tgt]
                        .find("select")
                        .val(v["mins"]).gentleSelect("update")
                        .end();
                } else {
                    block[tgt].find("select").val(v[tgt]).gentleSelect("update");
                }
            }

            // trigger change event
            block["period"].find("select")
                .val(t)
                .gentleSelect("update")
                .trigger("change");

            return this;
        }
    };

    var event_handlers = {
        periodChanged: function() {
            var root = $(this).data("root");
            var block = root.data("block"),
                opt = root.data("options");
            var period = $(this).val();
            root.find("span.cron-block").hide(); // first, hide all blocks
            if (toDisplay.hasOwnProperty(period)) { // not custom value
                var b = toDisplay[$(this).val()];
                for (var i = 0; i < b.length; i++) { block[b[i]].show(); }
            }
        },

        somethingChanged: function() {
            root = $(this).data("root");
            // if AJAX url defined, show "save"/"reset" button
            if (defined(root.data("options").url_set)) {
                if (methods.value.call(root) != root.data("current_value")) { // if changed
                    root.addClass("cron-changed");
                    root.data("block")["controls"].fadeIn();
                } else { // values manually reverted
                    root.removeClass("cron-changed");
                    root.data("block")["controls"].fadeOut();
                }
            } else { root.data("block")["controls"].hide(); }

            // chain in user defined event handler, if specified
            var oc = root.data("options").onChange;
            if (defined(oc) && $.isFunction(oc)) { oc.call(root); }
        },

        saveClicked: function() {
            var btn = $(this);
            var root = btn.data("root");
            var cron_str = methods.value.call(root);

            if (btn.hasClass("cron-loading")) { return; } // in progress
            btn.addClass("cron-loading");

            $.ajax({
                type: "POST",
                url: root.data("options").url_set,
                data: { "cron": cron_str },
                success: function() {
                    root.data("current_value", cron_str);
                    btn.removeClass("cron-loading");
                    // data changed since "save" clicked?
                    if (cron_str == methods.value.call(root)) {
                        root.removeClass("cron-changed");
                        root.data("block").controls.fadeOut();
                    }
                },
                error: function() {
                    alert("An error occured when submitting your request. Try again?");
                    btn.removeClass("cron-loading");
                }
            });
        }
    };

    $.fn.cron = function(method) {
        if (methods[method]) {
            return methods[method].apply(this, Array.prototype.slice.call(arguments, 1));
        } else if (typeof method === 'object' || !method) {
            return methods.init.apply(this, arguments);
        } else {
            $.error('Method ' + method + ' does not exist on jQuery.cron');
        }
    };

})(jQuery);