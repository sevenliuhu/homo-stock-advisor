/* Copyright (c) 2026 HOMO AI. Proprietary. License required. Contact: 16208204@qq.com */

const _key = process.env.HOMO_LICENSE_KEY;
if (!_key || _key.length < 16) {
    console.warn('[HOMO] License required. Commercial use needs a valid key. Contact: 16208204@qq.com');
}
module.exports = { validateLicense: () => _key && _key.length >= 16 };
