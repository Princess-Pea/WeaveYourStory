/**
 * 游戏素材配置表
 * 为三套游戏预设配置所需的场景、角色、互动元素素材
 */

import {
  generateSceneBackground,
  generateCharacterSprite,
  generateInteractiveElement,
  canvasToDataURL
} from '@/utils/pixelArtGenerator'

/**
 * 场景素材配置
 */
export const SCENE_ASSETS = {
  'scene_1': { // 森林入口
    type: 'forest_entrance',
    name: '翠绿森林入口',
    size: { width: 800, height: 600 }
  },
  'scene_2': { // 精灵草地
    type: 'spirit_grassland',
    name: '精灵草地',
    size: { width: 800, height: 600 }
  },
  'scene_3': { // 神圣泉水
    type: 'sacred_spring',
    name: '神圣泉水',
    size: { width: 800, height: 600 }
  },
  'scene_4': { // 古老遗迹
    type: 'ancient_ruins',
    name: '古老遗迹',
    size: { width: 800, height: 600 }
  },
  // 城市的秘密
  'city_scene_1': {
    type: 'reporter_office',
    name: '记者办公室',
    size: { width: 800, height: 600 }
  },
  'city_scene_2': {
    type: 'dark_street',
    name: '暗夜街道',
    size: { width: 800, height: 600 }
  },
  'city_scene_3': {
    type: 'underground_parking',
    name: '地下停车场',
    size: { width: 800, height: 600 }
  },
  'city_scene_4': {
    type: 'secret_lab',
    name: '秘密实验室',
    size: { width: 800, height: 600 }
  },
  // 光阴的故事
  'school_scene_1': {
    type: 'school_hall',
    name: '学院主堂',
    size: { width: 800, height: 600 }
  },
  'school_scene_2': {
    type: 'cherry_courtyard',
    name: '樱花庭院',
    size: { width: 800, height: 600 }
  },
  'school_scene_3': {
    type: 'library',
    name: '古老图书馆',
    size: { width: 800, height: 600 }
  },
  'school_scene_4': {
    type: 'moonlight_path',
    name: '月光小径',
    size: { width: 800, height: 600 }
  },
  'school_scene_5': {
    type: 'highest_tower',
    name: '校园最高塔',
    size: { width: 800, height: 600 }
  }
};

/**
 * 角色素材配置
 */
export const CHARACTER_ASSETS = {
  // 森林的守护者
  'char_1': { // 月影
    type: 'elf_female',
    name: '月影',
    size: 64
  },
  'char_2': { // 火狐
    type: 'fox_spirit',
    name: '火狐',
    size: 64
  },
  'char_3': { // 石谷
    type: 'dwarf_male',
    name: '石谷',
    size: 64
  },
  'char_4': { // 古董
    type: 'raven_wise',
    name: '古董',
    size: 64
  },
  // 城市的秘密
  'city_char_1': {
    type: 'young_reporter',
    name: '雷克斯',
    size: 64
  },
  'city_char_2': {
    type: 'mysterious_woman',
    name: '夜莺',
    size: 64
  },
  'city_char_3': {
    type: 'old_worker',
    name: '老赵',
    size: 64
  },
  'city_char_4': {
    type: 'mad_doctor',
    name: '博士',
    size: 64
  },
  // 光阴的故事
  'school_char_1': {
    type: 'school_girl',
    name: '君',
    size: 64
  },
  'school_char_2': {
    type: 'short_hair_friend',
    name: '林岚',
    size: 64
  },
  'school_char_3': {
    type: 'school_principal',
    name: '校长',
    size: 64
  },
  'school_char_4': {
    type: 'time_guardian',
    name: '时间守护者',
    size: 64
  }
};

/**
 * 互动元素素材配置
 */
export const ELEMENT_ASSETS = {
  // 森林的守护者
  'glowing_leaf': {
    type: 'glowing_leaf',
    name: '发光的树叶',
    size: 32
  },
  'blue_crystal': {
    type: 'blue_crystal',
    name: '青色水晶',
    size: 32
  },
  'contract_fragment': {
    type: 'contract_fragment',
    name: '灵兽契约碎片',
    size: 32
  },
  // 城市的秘密
  'mystery_letter': {
    type: 'letter',
    name: '神秘信件',
    size: 32
  },
  'pass_card': {
    type: 'pass',
    name: '通行证',
    size: 32
  },
  'evidence_file': {
    type: 'evidence_file',
    name: '证据文件',
    size: 32
  },
  // 光阴的故事
  'cherry_petal': {
    type: 'cherry_petal',
    name: '樱花花瓣',
    size: 32
  },
  'youth_diary': {
    type: 'diary',
    name: '青春日记',
    size: 32
  },
  'light': {
    type: 'light',
    name: '光',
    size: 32
  }
};

/**
 * 素材缓存
 */
const assetCache = new Map();

/**
 * 获取或生成场景背景
 * @param {string} sceneId - 场景ID
 * @returns {string} Data URL
 */
export function getSceneBackground(sceneId) {
  const cacheKey = `scene_${sceneId}`;
  
  if (assetCache.has(cacheKey)) {
    return assetCache.get(cacheKey);
  }

  const config = SCENE_ASSETS[sceneId];
  if (!config) {
    console.warn(`Scene ${sceneId} not found in configuration`);
    return null;
  }

  const canvas = generateSceneBackground(config.type, config.size.width, config.size.height);
  const dataUrl = canvasToDataURL(canvas);
  assetCache.set(cacheKey, dataUrl);
  return dataUrl;
}

/**
 * 获取或生成角色精灵
 * @param {string} charId - 角色ID
 * @returns {string} Data URL
 */
export function getCharacterSprite(charId) {
  const cacheKey = `char_${charId}`;
  
  if (assetCache.has(cacheKey)) {
    return assetCache.get(cacheKey);
  }

  const config = CHARACTER_ASSETS[charId];
  if (!config) {
    console.warn(`Character ${charId} not found in configuration`);
    return null;
  }

  const canvas = generateCharacterSprite(config.type, config.size);
  const dataUrl = canvasToDataURL(canvas);
  assetCache.set(cacheKey, dataUrl);
  return dataUrl;
}

/**
 * 获取或生成互动元素
 * @param {string} elementId - 元素ID
 * @returns {string} Data URL
 */
export function getInteractiveElement(elementId) {
  const cacheKey = `element_${elementId}`;
  
  if (assetCache.has(cacheKey)) {
    return assetCache.get(cacheKey);
  }

  const config = ELEMENT_ASSETS[elementId];
  if (!config) {
    console.warn(`Element ${elementId} not found in configuration`);
    return null;
  }

  const canvas = generateInteractiveElement(config.type, config.size);
  const dataUrl = canvasToDataURL(canvas);
  assetCache.set(cacheKey, dataUrl);
  return dataUrl;
}

/**
 * 预加载所有素材
 */
export function preloadAllAssets() {
  // 预加载场景
  Object.keys(SCENE_ASSETS).forEach(sceneId => {
    getSceneBackground(sceneId);
  });

  // 预加载角色
  Object.keys(CHARACTER_ASSETS).forEach(charId => {
    getCharacterSprite(charId);
  });

  // 预加载元素
  Object.keys(ELEMENT_ASSETS).forEach(elementId => {
    getInteractiveElement(elementId);
  });
}

/**
 * 清空素材缓存
 */
export function clearAssetCache() {
  assetCache.clear();
}

/**
 * 获取缓存统计
 */
export function getAssetCacheStats() {
  return {
    total: assetCache.size,
    items: Array.from(assetCache.keys())
  };
}

/**
 * 为游戏预设注入素材
 * @param {Object} gameData - 游戏数据
 * @returns {Object} 注入了素材的游戏数据
 */
export function injectAssets(gameData) {
  const enrichedGameData = JSON.parse(JSON.stringify(gameData));

  // 为场景注入背景图片
  if (enrichedGameData.scenes && Array.isArray(enrichedGameData.scenes)) {
    enrichedGameData.scenes.forEach((scene, index) => {
      scene.backgroundImage = getSceneBackground(`scene_${index + 1}`);
    });
  }

  // 为角色注入精灵图片
  if (enrichedGameData.characters && Array.isArray(enrichedGameData.characters)) {
    enrichedGameData.characters.forEach((character, index) => {
      character.sprite = getCharacterSprite(`char_${index + 1}`);
    });
  }

  // 为互动元素注入图片
  if (enrichedGameData.scenes && Array.isArray(enrichedGameData.scenes)) {
    enrichedGameData.scenes.forEach(scene => {
      if (scene.interactiveElements && Array.isArray(scene.interactiveElements)) {
        scene.interactiveElements.forEach(element => {
          // 根据元素名称推断元素ID
          const elementId = element.name
            ?.toLowerCase()
            ?.replace(/[^\w]/g, '_') || 'default';
          element.sprite = getInteractiveElement(elementId);
        });
      }
    });
  }

  return enrichedGameData;
}
