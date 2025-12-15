const chromium = require('@sparticuz/chromium');
const puppeteer = require('puppeteer-core');

// JST timezone offset (UTC+9)
const JST_OFFSET = 9 * 60 * 60 * 1000;

// Debug mode settings
const DEBUG_MODE = (process.env.DEBUG_MODE || 'false').toLowerCase() === 'true';
const DEBUG_DATE = process.env.DEBUG_DATE || '';

function debugLog(message) {
  if (DEBUG_MODE) {
    console.log(`[DEBUG] ${message}`);
  }
}

function getJSTDate() {
  const now = new Date();
  return new Date(now.getTime() + JST_OFFSET + now.getTimezoneOffset() * 60 * 1000);
}

function getTargetDate() {
  if (DEBUG_MODE && DEBUG_DATE) {
    const parsed = Date.parse(DEBUG_DATE + 'T00:00:00+09:00');
    if (!isNaN(parsed)) {
      return new Date(parsed);
    }
    console.log(`[DEBUG] Invalid DEBUG_DATE format: ${DEBUG_DATE}, using current date`);
  }
  return getJSTDate();
}

function formatDate(date) {
  const year = date.getFullYear();
  const month = String(date.getMonth() + 1).padStart(2, '0');
  const day = String(date.getDate()).padStart(2, '0');
  return `${year}-${month}-${day}`;
}

function getRowSelector(targetDate) {
  const dateStr = formatDate(targetDate);
  return `tr._js-${dateStr}`;
}

function extractMembersFromDescription(description) {
  if (!description) return '';
  const slashMatch = description.match(/^(.+?)／/);
  if (slashMatch) {
    return slashMatch[1].trim();
  }
  return description.trim();
}

function extractHosts(description, weekdayNumber) {
  description = description.trim();

  // "ホスト：" pattern (Friday, etc.)
  const hostMatch = description.match(/ホスト[：:]\s*(.+?)(?:／|$)/);
  if (hostMatch) {
    return hostMatch[1].trim();
  }

  // "進行：" pattern (Saturday, etc.)
  const progressMatch = description.match(/進行[：:]\s*(.+?)(?:\s+と(?:貴方|あなた)|／|$)/);
  if (progressMatch) {
    return progressMatch[1].trim();
  }

  // "〜と〜" pattern (normal jam session)
  const toMatch = description.match(/(.+?)と(.+?)(?:です|／|$)/);
  if (toMatch) {
    return toMatch[1].trim();
  }

  // Get part before "／"
  const slashMatch = description.match(/^(.+?)／/);
  if (slashMatch) {
    return slashMatch[1].trim();
  }

  return 'No Data';
}

function parseHtml(html, targetDate) {
  // Simple HTML parsing without external library
  const weekdayNumber = targetDate.getDay();
  // Convert JS weekday (0=Sunday) to Python-style (0=Monday)
  const pythonWeekday = weekdayNumber === 0 ? 6 : weekdayNumber - 1;

  debugLog(`Target date: ${formatDate(targetDate)} (weekday: ${pythonWeekday})`);

  // Check for table
  if (!html.includes('jazzScheduleTable')) {
    debugLog('Table .jazzScheduleTable not found');
    return 'No Data';
  }

  // Find row for target date
  const rowSelector = getRowSelector(targetDate);
  const rowClassPattern = `_js-${formatDate(targetDate)}`;
  debugLog(`Row selector: ${rowSelector}`);

  // Extract the row
  const rowRegex = new RegExp(`<tr[^>]*class="[^"]*${rowClassPattern}[^"]*"[^>]*>([\\s\\S]*?)</tr>`, 'i');
  const rowMatch = html.match(rowRegex);

  if (!rowMatch) {
    debugLog(`Row not found for ${rowSelector}`);
    return 'No Data';
  }

  const rowHtml = rowMatch[1];

  // Find intro cell (_js-shop-intro)
  const introCellRegex = /<td[^>]*class="[^"]*_js-shop-intro[^"]*"[^>]*>([\s\S]*?)<\/td>/i;
  const introCellMatch = rowHtml.match(introCellRegex);

  if (!introCellMatch) {
    debugLog('Intro cell not found');
    return 'No Data';
  }

  const cellHtml = introCellMatch[1];

  // Extract title
  const titleRegex = /<[^>]*class="[^"]*jazzScheduleTable__dataTitle[^"]*"[^>]*>([\s\S]*?)<\/[^>]+>/i;
  const titleMatch = cellHtml.match(titleRegex);
  const title = titleMatch ? titleMatch[1].replace(/<[^>]+>/g, '').trim() : '';

  // Extract description
  const descRegex = /<[^>]*class="[^"]*jazzScheduleTable__dataDescription[^"]*"[^>]*>([\s\S]*?)<\/[^>]+>/i;
  const descMatch = cellHtml.match(descRegex);
  const description = descMatch ? descMatch[1].replace(/<[^>]+>/g, '').trim() : '';

  debugLog(`Title: ${JSON.stringify(title)}`);
  debugLog(`Raw description: ${JSON.stringify(description)}`);

  // Special cases
  if (description.includes('安息日')) {
    return 'sabbath';
  }

  // New Year's Day
  if (targetDate.getMonth() === 0 && targetDate.getDate() === 1) {
    return ['closed', 'お正月休みです。'];
  }

  // Closed day check
  if (title.includes('休み') || title.includes('おやすみ')) {
    return ['closed', title];
  }

  // Monday check (pythonWeekday 0 = Monday)
  if (pythonWeekday === 0) {
    if (title.includes('安息日') && (!description || description.includes('安息日'))) {
      return 'monday_rest';
    }
    if (title.includes('ライブ') && title) {
      const members = extractMembersFromDescription(description);
      return ['special_live', title, members];
    }
    if (description) {
      return 'specialday';
    }
    return 'monday_rest';
  }

  if (description.includes('バータイム')) {
    return 'bartime';
  }

  // Extract host names
  const hosts = extractHosts(description, pythonWeekday);
  debugLog(`Extracted hosts: ${hosts}`);

  return hosts;
}

async function webscrape() {
  const targetDate = getTargetDate();

  debugLog(`Starting webscrape for date: ${formatDate(targetDate)}`);

  const browser = await puppeteer.launch({
    args: chromium.args,
    defaultViewport: chromium.defaultViewport,
    executablePath: await chromium.executablePath(),
    headless: chromium.headless,
  });

  try {
    const page = await browser.newPage();
    await page.goto('https://www.cafecottonclub.com/jazz/', {
      waitUntil: 'networkidle0',
      timeout: 30000,
    });

    // Wait for JavaScript to load
    await page.waitForSelector('.jazzScheduleTable', { timeout: 10000 });

    const html = await page.content();
    return parseHtml(html, targetDate);
  } finally {
    await browser.close();
  }
}

// Export for testing
module.exports = {
  webscrape,
  parseHtml,
  getTargetDate,
  formatDate,
  getRowSelector,
  extractHosts,
  DEBUG_MODE,
  DEBUG_DATE,
};
