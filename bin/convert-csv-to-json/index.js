#!/usr/bin/env node

var ASVS = {
    "chapterNames": {
        "2" : {
            "en": "Authentication"
        },
        "3" : {
            "en" : "Session Management"
        },
        "4" : {
            "en" : "Access Control"
        },
        "5" : {
            "en" : "Malicious Input Handling"
        },
        "7": {
            "en": "Cryptography at Rest"
        },
        "8": {
            "en": "Error Handling and Logging"
        },
        "9": {
            "en": "Data Protection"
        },
        "10": {
            "en": "Communications"
        },
        "11": {
            "en": "HTTP"
        },
        "13": {
            "en": "Malicious Controls"
        },
        "15": {
            "en": "Business Logic"
        },
        "16": {
            "en": "File and Resource"
        },
        "17": {
            "en": "Mobile"
        }
    },
    "levelNames": {
        "0": {
            "en": "Cursory"
        },
        "1": {
            "en": "Opportunistic"
        },
        "2": {
            "en": "Standard"
        },
        "3": {
            "en": "Advanced"
        }
    },
    "requirements": [
//        {
//            "chapterNr": "1",
//            "nr": "1",
//            "levels": ["1", "2"],
//            "title": {
//                "en": "Verify that all application components",
//                  "fr": "..."
//            }
//        }
    ]
};

var program = require('commander');

program
    .version('0.0.1')
    .usage('<from-file> <to-file>')
    .parse(process.argv);

if(program.args.length < 2) {
    program.help();
    return;
}

var file = program.args[0];
fs = require('fs');

var content = fs.readFileSync(file, 'utf8');

require('csv').parse(content, {delimiter: "\t"}, function(err, output) {
    if (err) {
        throw err;
    }
    // Remove the header.
    output.shift();

    ASVS.requirements = output.map(function(requirement) {
        var numbers = /V(\d+).(\d+)/.exec(requirement[0]);

        var h1 = numbers[1];
        var h2 = numbers[2];
        var en = requirement[1];
        var fr = requirement[2];

        return { "chapterNr": h1, "nr": h2, "title": { "en" : en, "fr" : fr}};
    });

    fs.writeFileSync(program.args[1], JSON.stringify(ASVS, null, 4));
});

