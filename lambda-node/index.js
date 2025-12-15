const { TwitterApi } = require('twitter-api-v2');
const { webscrape, getTargetDate, DEBUG_MODE } = require('./webscrape');

const BEARER_TOKEN = process.env.BEARER_TOKEN || '';
const API_KEY = process.env.API_KEY || '';
const API_KEY_SECRET = process.env.API_KEY_SECRET || '';
const ACCESS_TOKEN = process.env.ACCESS_TOKEN || '';
const ACCESS_TOKEN_SECRET = process.env.ACCESS_TOKEN_SECRET || '';

function debugLog(message) {
  if (DEBUG_MODE) {
    console.log(`[DEBUG] ${message}`);
  }
}

function getDay(targetDate) {
  // JavaScript: 0=Sunday, 1=Monday, ..., 6=Saturday
  const weekdayNumber = targetDate.getDay();
  const weekdays = ['日', '月', '火', '水', '木', '金', '土'];
  return weekdays[weekdayNumber];
}

function getDate(targetDate) {
  const month = targetDate.getMonth() + 1;
  const day = targetDate.getDate();
  return `${month}月${day}日`;
}

async function handler(event, context) {
  const musiciansName = await webscrape();
  const targetDate = getTargetDate();

  const tweetDatePart = getDate(targetDate) + '(' + getDay(targetDate) + ')';
  const dayOfWeek = getDay(targetDate);

  let tweet;

  if (musiciansName === 'bartime') {
    tweet = tweetDatePart + 'はバータイム営業です';
  } else if (musiciansName === 'sabbath') {
    tweet = tweetDatePart + 'はイントロとゴッド井上の安息日です。';
  } else if (musiciansName === 'monday_rest') {
    tweet = tweetDatePart + 'はゴッドの安息日です。ジャムセッションはおやすみです。';
  } else if (Array.isArray(musiciansName) && musiciansName[0] === 'special_live') {
    // Special live: [special_live, title, members]
    const [, liveTitle, members] = musiciansName;
    tweet = tweetDatePart + 'は\n' + liveTitle + '\n' + members + '\nhttps://www.cafecottonclub.com/jazz/';
  } else if (Array.isArray(musiciansName) && musiciansName[0] === 'closed') {
    // Closed day: [closed, title]
    const [, closedTitle] = musiciansName;
    tweet = tweetDatePart + 'は' + closedTitle;
  } else if (musiciansName === 'specialday') {
    tweet = tweetDatePart + 'は特別営業の日です。\n詳しくはHPをご確認ください。\nhttps://www.cafecottonclub.com/jazz/';
  } else if (dayOfWeek === '金') {
    tweet = tweetDatePart + 'の花金ジャズライブ＆セッションは\n' + musiciansName + 'です。';
  } else if (dayOfWeek === '土') {
    tweet = tweetDatePart + 'のジャムセッションホストは\n' + musiciansName + 'です。';
  } else if (dayOfWeek === '水' || dayOfWeek === '木') {
    tweet = tweetDatePart + 'のジャムセッションホストは\n' + 'ゴッド井上as ' + musiciansName + 'です。';
  } else {
    tweet = tweetDatePart + 'のジャムセッションホストは\n' + 'ゴッド井上as ' + musiciansName + 'です。';
  }

  console.log('---TWEET---');
  console.log(tweet);

  if (DEBUG_MODE) {
    debugLog('Tweet not sent (DEBUG_MODE is enabled)');
    return { statusCode: 200, body: tweet };
  }

  const client = new TwitterApi({
    appKey: API_KEY,
    appSecret: API_KEY_SECRET,
    accessToken: ACCESS_TOKEN,
    accessSecret: ACCESS_TOKEN_SECRET,
  });

  await client.v2.tweet(tweet);
  return { statusCode: 200, body: 'Tweet sent' };
}

module.exports = { handler };
