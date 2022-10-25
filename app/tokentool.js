// Note: this tool is not all-encompassing. Its mostly me not wanting to repeat requests I've done and keep things saved everywhere

import got from 'got';
import readline from 'readline-sync';
import fs from 'fs';

// This function checks if (for example) an userid is saved. If not, it prompts for it.
function param(key) {
    let dataFilename = `secret.${key}.txt`;
    try {
        return fs.readFileSync(dataFilename, {encoding: "utf-8"});
    } catch {
        let data = readline.question(`Enter ${key}: `);
        fs.writeFileSync(dataFilename, data, {encoding: "utf-8"});
        return data;
    }
}
// This function sends a request to Facebooks API
function requestToken(tokenname, url) {
    let dataFilename = `secret.${key}.json`;

    fs.writeFileSync(dataFilename, data, {encoding: "utf-8"});

    got.get()
    
}

//requestToken(`https://graph.facebook.com/${param("userid")}/accounts?access_token=${param("useraccesstoken")}`)

"https://graph.facebook.com/PAGE-ID?fields=access_token&access_token=USER-ACCESS-TOKEN"
