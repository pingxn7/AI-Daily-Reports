// 简单的测试脚本来验证 API 客户端
import { apiClient } from './lib/api.ts';

async function test() {
  try {
    console.log('Testing API client...');
    console.log('API URL:', process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000');

    const summary = await apiClient.getSummaryById(4);
    console.log('✓ API call successful');
    console.log('Summary ID:', summary.id);
    console.log('Date:', summary.date);
    console.log('Highlights:', summary.highlights?.length);
    console.log('Other news:', summary.other_news?.length);
  } catch (error) {
    console.error('✗ API call failed:', error.message);
    if (error.response) {
      console.error('Response status:', error.response.status);
      console.error('Response data:', error.response.data);
    }
  }
}

test();
