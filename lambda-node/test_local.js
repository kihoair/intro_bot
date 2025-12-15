/**
 * Local test script for intro-tweet-bot
 *
 * Usage:
 *   node test_local.js                    # Test with today's date
 *   DEBUG_DATE=2025-12-20 node test_local.js  # Test with specific date
 */

// Set DEBUG_MODE for testing
process.env.DEBUG_MODE = 'true';

const { parseHtml, getTargetDate, formatDate, getRowSelector, DEBUG_MODE, DEBUG_DATE } = require('./webscrape');

// Sample HTML for testing (simulates website structure)
function generateTestHtml(dateStr, title, description) {
  return `
<!DOCTYPE html>
<html>
<body>
<table class="jazzScheduleTable">
  <tr class="_js-${dateStr}">
    <td class="_js-shop-intro">
      <div class="jazzScheduleTable__dataTitle">${title}</div>
      <div class="jazzScheduleTable__dataDescription">${description}</div>
    </td>
  </tr>
</table>
</body>
</html>
`;
}

async function runTests() {
  console.log('=== intro-tweet-bot Local Test ===');
  console.log(`DEBUG_MODE: ${DEBUG_MODE}`);
  console.log(`DEBUG_DATE: ${DEBUG_DATE || '(not set, using current date)'}`);
  console.log('');

  const targetDate = getTargetDate();
  const dateStr = formatDate(targetDate);
  const rowSelector = getRowSelector(targetDate);

  console.log(`Target date: ${dateStr}`);
  console.log(`Row selector: ${rowSelector}`);
  console.log(`Weekday: ${targetDate.getDay()} (JS: 0=Sun, 1=Mon...)`);
  console.log('');

  // Test cases
  const testCases = [
    {
      name: 'Normal weekday (Tuesday-Thursday)',
      title: '',
      description: 'ゴッド井上as REIKOp と誰々です／1500円',
      expected: 'ゴッド井上as REIKOp',
    },
    {
      name: 'Friday (host pattern)',
      title: '',
      description: 'ホスト：山田太郎tp 鈴木花子p／2000円',
      expected: '山田太郎tp 鈴木花子p',
    },
    {
      name: 'Saturday (progress pattern)',
      title: '',
      description: '進行：ゴッド井上as ホルヘシローb と貴方／1500円',
      expected: 'ゴッド井上as ホルヘシローb',
    },
    {
      name: 'Sabbath (安息日)',
      title: '',
      description: '安息日',
      expected: 'sabbath',
    },
    {
      name: 'Bar time',
      title: '',
      description: 'バータイム',
      expected: 'bartime',
    },
    {
      name: 'Closed day',
      title: '年末おやすみ',
      description: '',
      expected: ['closed', '年末おやすみ'],
    },
  ];

  console.log('=== Running Test Cases ===');
  for (const testCase of testCases) {
    const html = generateTestHtml(dateStr, testCase.title, testCase.description);
    const result = parseHtml(html, targetDate);

    const passed = JSON.stringify(result) === JSON.stringify(testCase.expected);
    const status = passed ? 'PASS' : 'FAIL';

    console.log(`[${status}] ${testCase.name}`);
    console.log(`  Input: title="${testCase.title}", desc="${testCase.description}"`);
    console.log(`  Expected: ${JSON.stringify(testCase.expected)}`);
    console.log(`  Got: ${JSON.stringify(result)}`);
    console.log('');
  }

  console.log('=== Test Complete ===');
}

runTests().catch(console.error);
