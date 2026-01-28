/**
 * 像素风图片生成工具
 * 用于动态生成游戏中的场景、角色等像素风素材
 */

/**
 * 创建一个像素风场景背景（Canvas）
 * @param {string} sceneType - 场景类型: 'forest', 'city', 'school'
 * @param {number} width - 宽度
 * @param {number} height - 高度
 * @returns {HTMLCanvasElement} Canvas对象
 */
export function generateSceneBackground(sceneType, width = 800, height = 600) {
  const canvas = document.createElement('canvas');
  canvas.width = width;
  canvas.height = height;
  const ctx = canvas.getContext('2d');

  switch (sceneType) {
    case 'forest_entrance':
      drawForestEntrance(ctx, width, height);
      break;
    case 'spirit_grassland':
      drawSpiritGrassland(ctx, width, height);
      break;
    case 'sacred_spring':
      drawSacredSpring(ctx, width, height);
      break;
    case 'ancient_ruins':
      drawAncientRuins(ctx, width, height);
      break;
    case 'reporter_office':
      drawReporterOffice(ctx, width, height);
      break;
    case 'dark_street':
      drawDarkStreet(ctx, width, height);
      break;
    case 'underground_parking':
      drawUndergroundParking(ctx, width, height);
      break;
    case 'secret_lab':
      drawSecretLab(ctx, width, height);
      break;
    case 'school_hall':
      drawSchoolHall(ctx, width, height);
      break;
    case 'cherry_courtyard':
      drawCherryCourtyard(ctx, width, height);
      break;
    case 'library':
      drawLibrary(ctx, width, height);
      break;
    case 'moonlight_path':
      drawMoonlightPath(ctx, width, height);
      break;
    case 'highest_tower':
      drawHighestTower(ctx, width, height);
      break;
    default:
      drawDefaultScene(ctx, width, height);
  }

  return canvas;
}

/**
 * 创建一个像素风角色（Canvas）
 * @param {string} characterType - 角色类型
 * @param {number} size - 大小（像素）
 * @returns {HTMLCanvasElement} Canvas对象
 */
export function generateCharacterSprite(characterType, size = 64) {
  const canvas = document.createElement('canvas');
  canvas.width = size;
  canvas.height = size;
  const ctx = canvas.getContext('2d');

  switch (characterType) {
    case 'elf_female':
      drawElfFemale(ctx, size);
      break;
    case 'dwarf_male':
      drawDwarfMale(ctx, size);
      break;
    case 'fox_spirit':
      drawFoxSpirit(ctx, size);
      break;
    case 'raven_wise':
      drawRavenWise(ctx, size);
      break;
    case 'young_reporter':
      drawYoungReporter(ctx, size);
      break;
    case 'mysterious_woman':
      drawMysteriousWoman(ctx, size);
      break;
    case 'old_worker':
      drawOldWorker(ctx, size);
      break;
    case 'mad_doctor':
      drawMadDoctor(ctx, size);
      break;
    case 'school_girl':
      drawSchoolGirl(ctx, size);
      break;
    case 'short_hair_friend':
      drawShortHairFriend(ctx, size);
      break;
    case 'school_principal':
      drawSchoolPrincipal(ctx, size);
      break;
    case 'time_guardian':
      drawTimeGuardian(ctx, size);
      break;
    default:
      drawDefaultCharacter(ctx, size);
  }

  return canvas;
}

/**
 * 创建一个像素风互动元素（Canvas）
 * @param {string} elementType - 元素类型: 'npc', 'item', 'obstacle'
 * @param {number} size - 大小
 * @returns {HTMLCanvasElement} Canvas对象
 */
export function generateInteractiveElement(elementType, size = 32) {
  const canvas = document.createElement('canvas');
  canvas.width = size;
  canvas.height = size;
  const ctx = canvas.getContext('2d');

  switch (elementType) {
    case 'glowing_leaf':
      drawGlowingLeaf(ctx, size);
      break;
    case 'blue_crystal':
      drawBlueCrystal(ctx, size);
      break;
    case 'contract_fragment':
      drawContractFragment(ctx, size);
      break;
    case 'letter':
      drawLetter(ctx, size);
      break;
    case 'pass':
      drawPass(ctx, size);
      break;
    case 'evidence_file':
      drawEvidenceFile(ctx, size);
      break;
    case 'cherry_petal':
      drawCherryPetal(ctx, size);
      break;
    case 'diary':
      drawDiary(ctx, size);
      break;
    case 'light':
      drawLight(ctx, size);
      break;
    default:
      drawDefaultElement(ctx, size);
  }

  return canvas;
}

// ===== 场景绘制函数 =====

function drawForestEntrance(ctx, w, h) {
  // 天空渐变
  const grad = ctx.createLinearGradient(0, 0, 0, h);
  grad.addColorStop(0, '#87CEEB');
  grad.addColorStop(1, '#B8D4E8');
  ctx.fillStyle = grad;
  ctx.fillRect(0, 0, w, h);

  // 地面
  ctx.fillStyle = '#558B2F';
  ctx.fillRect(0, h - 100, w, 100);

  // 远山
  ctx.fillStyle = '#6B8E23';
  drawPixelTriangle(ctx, w * 0.1, h - 100, 80, 120);
  drawPixelTriangle(ctx, w * 0.4, h - 100, 100, 150);
  drawPixelTriangle(ctx, w * 0.7, h - 100, 80, 120);

  // 树
  drawPixelTree(ctx, w * 0.25, h - 150, 40, 80, '#228B22');
  drawPixelTree(ctx, w * 0.75, h - 140, 50, 100, '#2E8B57');

  // 发光精灵草
  for (let i = 0; i < 8; i++) {
    const x = (w / 9) * (i + 1);
    const y = h - 80 + Math.sin(i) * 20;
    ctx.fillStyle = '#7FFFD4';
    ctx.fillRect(x - 4, y - 4, 8, 8);
    ctx.fillStyle = '#00FFFF';
    ctx.fillRect(x - 2, y - 2, 4, 4);
  }

  // 阳光
  ctx.fillStyle = '#FFD700';
  ctx.beginPath();
  ctx.arc(w - 80, 60, 50, 0, Math.PI * 2);
  ctx.fill();
  ctx.fillStyle = '#FFED4E';
  ctx.beginPath();
  ctx.arc(w - 80, 60, 45, 0, Math.PI * 2);
  ctx.fill();
}

function drawSpiritGrassland(ctx, w, h) {
  // 天空
  const grad = ctx.createLinearGradient(0, 0, 0, h);
  grad.addColorStop(0, '#87CEEB');
  grad.addColorStop(1, '#90EE90');
  ctx.fillStyle = grad;
  ctx.fillRect(0, 0, w, h);

  // 地面
  ctx.fillStyle = '#7CFC00';
  ctx.fillRect(0, h - 80, w, 80);

  // 巨大樱花树
  ctx.fillStyle = '#8B4513';
  ctx.fillRect(w / 2 - 30, h - 200, 60, 120);
  ctx.fillStyle = '#FF69B4';
  drawPixelCircle(ctx, w / 2, h - 200, 80);

  // 樱花花瓣飘落效果
  ctx.fillStyle = 'rgba(255, 192, 203, 0.7)';
  for (let i = 0; i < 15; i++) {
    const x = Math.random() * w;
    const y = Math.random() * h;
    drawPixelFlower(ctx, x, y, 3);
  }

  // 古老石碑
  ctx.fillStyle = '#808080';
  ctx.fillRect(w * 0.15 - 15, h - 120, 30, 80);
  ctx.fillStyle = '#A9A9A9';
  ctx.fillRect(w * 0.15 - 10, h - 110, 20, 20);
}

function drawSacredSpring(ctx, w, h) {
  // 昏暗天空
  const grad = ctx.createLinearGradient(0, 0, 0, h);
  grad.addColorStop(0, '#4A5568');
  grad.addColorStop(1, '#2D3748');
  ctx.fillStyle = grad;
  ctx.fillRect(0, 0, w, h);

  // 地面
  ctx.fillStyle = '#5A6370';
  ctx.fillRect(0, h - 80, w, 80);

  // 泉水
  ctx.fillStyle = '#E0FFFF';
  drawPixelCircle(ctx, w / 2, h - 120, 100);
  ctx.fillStyle = '#00FFFF';
  drawPixelCircle(ctx, w / 2, h - 120, 90);

  // 石头祭坛
  ctx.fillStyle = '#696969';
  for (let i = 0; i < 3; i++) {
    ctx.fillRect(w / 2 - 60 + i * 50, h - 100 - i * 20, 40, 40 + i * 20);
  }

  // 发光效果
  ctx.fillStyle = 'rgba(0, 255, 255, 0.3)';
  drawPixelCircle(ctx, w / 2, h - 120, 130);
}

function drawAncientRuins(ctx, w, h) {
  // 夜间背景
  const grad = ctx.createLinearGradient(0, 0, 0, h);
  grad.addColorStop(0, '#1a1a2e');
  grad.addColorStop(1, '#0f3460');
  ctx.fillStyle = grad;
  ctx.fillRect(0, 0, w, h);

  // 地面
  ctx.fillStyle = '#4A5568';
  ctx.fillRect(0, h - 80, w, 80);

  // 破旧柱子
  ctx.fillStyle = '#8B7355';
  for (let i = 0; i < 4; i++) {
    ctx.fillRect(w * 0.2 + i * 150, h - 200, 40, 150);
  }

  // 蘑菇
  ctx.fillStyle = '#D2B48C';
  for (let i = 0; i < 6; i++) {
    const x = Math.random() * w;
    const y = h - 100 + Math.random() * 20;
    drawPixelMushroom(ctx, x, y, 8);
  }

  // 星星
  ctx.fillStyle = '#FFFF00';
  for (let i = 0; i < 20; i++) {
    const x = Math.random() * w;
    const y = Math.random() * (h * 0.5);
    ctx.fillRect(x, y, 2, 2);
  }
}

function drawReporterOffice(ctx, w, h) {
  // 室内背景
  const grad = ctx.createLinearGradient(0, 0, 0, h);
  grad.addColorStop(0, '#8B7355');
  grad.addColorStop(1, '#A0826D');
  ctx.fillStyle = grad;
  ctx.fillRect(0, 0, w, h);

  // 窗户
  ctx.fillStyle = '#1a1a1a';
  ctx.fillRect(w - 120, 20, 100, 80);
  ctx.fillStyle = '#4169E1';
  ctx.fillRect(w - 115, 25, 45, 35);
  ctx.fillRect(w - 65, 25, 45, 35);
  ctx.fillRect(w - 115, 65, 45, 35);
  ctx.fillRect(w - 65, 65, 45, 35);

  // 纸堆
  for (let i = 0; i < 8; i++) {
    ctx.fillStyle = '#F5F5F5';
    ctx.fillRect(50 + i * 15, 150 + i * 10, 100, 8);
  }

  // 线索板
  ctx.fillStyle = '#8B4513';
  ctx.fillRect(50, 300, 200, 150);
  ctx.fillStyle = '#DC143C';
  ctx.fillRect(60, 310, 180, 10);
  for (let i = 0; i < 8; i++) {
    ctx.fillStyle = '#FFD700';
    ctx.fillRect(70 + i * 20, 330, 10, 100);
  }
}

function drawDarkStreet(ctx, w, h) {
  // 夜间城市背景
  const grad = ctx.createLinearGradient(0, 0, 0, h);
  grad.addColorStop(0, '#0f0f1e');
  grad.addColorStop(1, '#1a1a2e');
  ctx.fillStyle = grad;
  ctx.fillRect(0, 0, w, h);

  // 地面
  ctx.fillStyle = '#2a2a3e';
  ctx.fillRect(0, h - 80, w, 80);

  // 霓虹灯塔楼
  ctx.fillStyle = '#2C2C54';
  ctx.fillRect(30, 50, 120, 400);
  ctx.fillRect(w - 150, 80, 120, 380);

  // 霓虹窗户
  ctx.strokeStyle = '#FF1493';
  ctx.lineWidth = 2;
  for (let i = 0; i < 10; i++) {
    for (let j = 0; j < 3; j++) {
      ctx.strokeRect(45 + j * 35, 60 + i * 40, 25, 25);
    }
  }

  // 路灯
  ctx.fillStyle = '#FFD700';
  ctx.beginPath();
  ctx.arc(w / 2, 80, 15, 0, Math.PI * 2);
  ctx.fill();
}

function drawUndergroundParking(ctx, w, h) {
  // 昏暗混凝土背景
  const grad = ctx.createLinearGradient(0, 0, 0, h);
  grad.addColorStop(0, '#4A4A4A');
  grad.addColorStop(1, '#2C2C2C');
  ctx.fillStyle = grad;
  ctx.fillRect(0, 0, w, h);

  // 停车场线条
  ctx.strokeStyle = '#FFD700';
  ctx.lineWidth = 2;
  for (let i = 0; i < 6; i++) {
    ctx.beginPath();
    ctx.moveTo(0, h / 6 * (i + 1));
    ctx.lineTo(w, h / 6 * (i + 1));
    ctx.stroke();
  }

  // 警报灯
  ctx.fillStyle = '#FF0000';
  ctx.beginPath();
  ctx.arc(w - 30, 30, 12, 0, Math.PI * 2);
  ctx.fill();
  ctx.fillStyle = '#FFB6C1';
  ctx.beginPath();
  ctx.arc(w - 30, 30, 8, 0, Math.PI * 2);
  ctx.fill();
}

function drawSecretLab(ctx, w, h) {
  // 高科技背景
  const grad = ctx.createLinearGradient(0, 0, 0, h);
  grad.addColorStop(0, '#001a4d');
  grad.addColorStop(1, '#003d99');
  ctx.fillStyle = grad;
  ctx.fillRect(0, 0, w, h);

  // 液体管道
  ctx.strokeStyle = '#00FF00';
  ctx.lineWidth = 3;
  ctx.beginPath();
  ctx.moveTo(0, h / 2);
  ctx.lineTo(w, h / 2);
  ctx.stroke();

  // 设备
  ctx.fillStyle = '#1a1a1a';
  ctx.fillRect(50, 50, 150, 200);
  ctx.fillStyle = '#00FF00';
  for (let i = 0; i < 8; i++) {
    ctx.fillRect(60 + i * 15, 60 + i * 10, 12, 12);
  }

  // 玻璃舱
  ctx.strokeStyle = '#00FFFF';
  ctx.lineWidth = 3;
  ctx.strokeRect(w - 200, h / 2 - 80, 150, 160);
  ctx.fillStyle = 'rgba(0, 255, 255, 0.1)';
  ctx.fillRect(w - 200, h / 2 - 80, 150, 160);
}

function drawSchoolHall(ctx, w, h) {
  // 宽敞的校舍背景
  const grad = ctx.createLinearGradient(0, 0, 0, h);
  grad.addColorStop(0, '#D4A574');
  grad.addColorStop(1, '#B8860B');
  ctx.fillStyle = grad;
  ctx.fillRect(0, 0, w, h);

  // 木质地板
  ctx.fillStyle = '#8B4513';
  for (let i = 0; i < w; i += 20) {
    ctx.fillRect(i, h - 100, 20, 10);
    ctx.fillRect(i, h - 50, 20, 10);
  }

  // 彩色窗户
  ctx.fillStyle = '#FF6347';
  ctx.fillRect(20, 20, 60, 80);
  ctx.fillStyle = '#4169E1';
  ctx.fillRect(100, 20, 60, 80);
  ctx.fillStyle = '#32CD32';
  ctx.fillRect(180, 20, 60, 80);

  // 照片框（过去的学生照片）
  ctx.fillStyle = '#D4A574';
  for (let i = 0; i < 4; i++) {
    for (let j = 0; j < 3; j++) {
      ctx.fillRect(50 + i * 150, 150 + j * 100, 100, 80);
      ctx.fillStyle = '#696969';
      ctx.fillRect(55 + i * 150, 155 + j * 100, 90, 70);
      ctx.fillStyle = '#D4A574';
    }
  }
}

function drawCherryCourtyard(ctx, w, h) {
  // 樱花庭院
  const grad = ctx.createLinearGradient(0, 0, 0, h);
  grad.addColorStop(0, '#FFB6C1');
  grad.addColorStop(1, '#FFC0CB');
  ctx.fillStyle = grad;
  ctx.fillRect(0, 0, w, h);

  // 地面
  ctx.fillStyle = '#D2B48C';
  ctx.fillRect(0, h - 100, w, 100);

  // 古老樱花树
  ctx.fillStyle = '#8B4513';
  ctx.fillRect(w / 2 - 40, h - 300, 80, 200);
  ctx.fillStyle = '#FF69B4';
  drawPixelCircle(ctx, w / 2, h - 300, 100);
  ctx.fillStyle = '#FFB6C1';
  drawPixelCircle(ctx, w / 2, h - 300, 85);

  // 樱花花瓣飘落
  ctx.fillStyle = 'rgba(255, 105, 180, 0.6)';
  for (let i = 0; i < 20; i++) {
    const x = Math.random() * w;
    const y = Math.random() * h;
    drawPixelFlower(ctx, x, y, 4);
  }

  // 小径
  ctx.fillStyle = '#D2691E';
  for (let i = 0; i < w; i += 30) {
    ctx.fillRect(i, h - 120, 25, 20);
  }
}

function drawLibrary(ctx, w, h) {
  // 图书馆背景
  const grad = ctx.createLinearGradient(0, 0, 0, h);
  grad.addColorStop(0, '#8B7355');
  grad.addColorStop(1, '#D2B48C');
  ctx.fillStyle = grad;
  ctx.fillRect(0, 0, w, h);

  // 书架
  ctx.fillStyle = '#654321';
  for (let i = 0; i < 5; i++) {
    ctx.fillRect(20, 80 + i * 80, w - 40, 15);
    for (let j = 0; j < 15; j++) {
      ctx.fillStyle = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#FFA502', '#2C3E50'][Math.floor(Math.random() * 5)];
      ctx.fillRect(30 + j * 50, 90 + i * 80, 40, 60);
    }
  }

  // 高窗户
  ctx.fillStyle = '#87CEEB';
  for (let i = 0; i < 3; i++) {
    ctx.fillRect(w - 80, 20 + i * 60, 60, 50);
  }
}

function drawMoonlightPath(ctx, w, h) {
  // 月光下的小径
  const grad = ctx.createLinearGradient(0, 0, 0, h);
  grad.addColorStop(0, '#191970');
  grad.addColorStop(1, '#2F4F4F');
  ctx.fillStyle = grad;
  ctx.fillRect(0, 0, w, h);

  // 月亮
  ctx.fillStyle = '#FFFACD';
  ctx.beginPath();
  ctx.arc(w - 80, 60, 50, 0, Math.PI * 2);
  ctx.fill();

  // 星星
  ctx.fillStyle = '#FFFF00';
  for (let i = 0; i < 30; i++) {
    const x = Math.random() * w;
    const y = Math.random() * (h * 0.6);
    ctx.fillRect(x, y, 2, 2);
  }

  // 小径
  ctx.fillStyle = '#D2B48C';
  ctx.beginPath();
  ctx.moveTo(w / 2, h);
  ctx.lineTo(w / 2 - 50, h - 100);
  ctx.lineTo(w / 2 + 50, h - 200);
  ctx.lineTo(w / 2 - 30, h - 300);
  ctx.lineTo(w / 2, 0);
  ctx.lineWidth = 60;
  ctx.stroke();

  // 樱花树
  for (let i = 0; i < 5; i++) {
    const x = w * 0.2 + i * w * 0.15;
    ctx.fillStyle = '#FF69B4';
    drawPixelCircle(ctx, x, h - 150 + Math.random() * 100, 30);
  }
}

function drawHighestTower(ctx, w, h) {
  // 塔顶夜空
  const grad = ctx.createLinearGradient(0, 0, 0, h);
  grad.addColorStop(0, '#000033');
  grad.addColorStop(1, '#330066');
  ctx.fillStyle = grad;
  ctx.fillRect(0, 0, w, h);

  // 星辰
  ctx.fillStyle = '#FFFFFF';
  for (let i = 0; i < 50; i++) {
    const x = Math.random() * w;
    const y = Math.random() * (h * 0.8);
    ctx.fillRect(x, y, 1, 1);
  }

  // 月光柱
  ctx.fillStyle = 'rgba(255, 250, 205, 0.3)';
  ctx.fillRect(0, 0, w, h);

  // 两个身影
  ctx.fillStyle = '#2C2C54';
  ctx.fillRect(w / 3, h / 2 + 50, 40, 80);
  ctx.fillRect(2 * w / 3 - 40, h / 2 + 50, 40, 80);

  // 围栏
  ctx.strokeStyle = '#FFD700';
  ctx.lineWidth = 2;
  ctx.beginPath();
  ctx.moveTo(0, h / 2);
  ctx.lineTo(w, h / 2);
  ctx.stroke();
}

function drawDefaultScene(ctx, w, h) {
  const grad = ctx.createLinearGradient(0, 0, 0, h);
  grad.addColorStop(0, '#87CEEB');
  grad.addColorStop(1, '#90EE90');
  ctx.fillStyle = grad;
  ctx.fillRect(0, 0, w, h);
}

// ===== 角色绘制函数 =====

function drawElfFemale(ctx, size) {
  const scale = size / 64;
  
  // 头
  ctx.fillStyle = '#FFD4A3';
  ctx.fillRect(18 * scale, 8 * scale, 28 * scale, 28 * scale);
  
  // 头发
  ctx.fillStyle = '#C0C0C0';
  ctx.fillRect(16 * scale, 6 * scale, 32 * scale, 8 * scale);
  
  // 眼睛
  ctx.fillStyle = '#000000';
  ctx.fillRect(24 * scale, 18 * scale, 4 * scale, 4 * scale);
  ctx.fillRect(36 * scale, 18 * scale, 4 * scale, 4 * scale);
  
  // 身体
  ctx.fillStyle = '#E6D4B8';
  ctx.fillRect(20 * scale, 36 * scale, 24 * scale, 20 * scale);
  
  // 衣服
  ctx.fillStyle = '#8B7BA8';
  ctx.fillRect(18 * scale, 38 * scale, 28 * scale, 16 * scale);
  
  // 腿
  ctx.fillStyle = '#FFD4A3';
  ctx.fillRect(22 * scale, 54 * scale, 8 * scale, 10 * scale);
  ctx.fillRect(34 * scale, 54 * scale, 8 * scale, 10 * scale);
}

function drawDwarfMale(ctx, size) {
  const scale = size / 64;
  
  // 头
  ctx.fillStyle = '#FFD4A3';
  ctx.fillRect(20 * scale, 12 * scale, 24 * scale, 20 * scale);
  
  // 胡须
  ctx.fillStyle = '#8B7355';
  ctx.fillRect(18 * scale, 28 * scale, 28 * scale, 6 * scale);
  
  // 身体
  ctx.fillStyle = '#654321';
  ctx.fillRect(18 * scale, 32 * scale, 28 * scale, 24 * scale);
  
  // 腿（短）
  ctx.fillStyle = '#8B4513';
  ctx.fillRect(22 * scale, 54 * scale, 8 * scale, 8 * scale);
  ctx.fillRect(34 * scale, 54 * scale, 8 * scale, 8 * scale);
}

function drawFoxSpirit(ctx, size) {
  const scale = size / 64;
  
  // 身体
  ctx.fillStyle = '#FF8C00';
  ctx.beginPath();
  ctx.arc(32 * scale, 40 * scale, 18 * scale, 0, Math.PI * 2);
  ctx.fill();
  
  // 尾巴
  ctx.fillStyle = '#FFB347';
  ctx.beginPath();
  ctx.arc(48 * scale, 38 * scale, 12 * scale, 0, Math.PI * 2);
  ctx.fill();
  
  // 头
  ctx.fillStyle = '#FF8C00';
  ctx.beginPath();
  ctx.arc(32 * scale, 24 * scale, 14 * scale, 0, Math.PI * 2);
  ctx.fill();
  
  // 耳朵
  ctx.fillStyle = '#FF6347';
  ctx.fillRect(20 * scale, 8 * scale, 8 * scale, 12 * scale);
  ctx.fillRect(44 * scale, 8 * scale, 8 * scale, 12 * scale);
  
  // 眼睛
  ctx.fillStyle = '#000000';
  ctx.fillRect(28 * scale, 22 * scale, 4 * scale, 4 * scale);
  ctx.fillRect(36 * scale, 22 * scale, 4 * scale, 4 * scale);
}

function drawRavenWise(ctx, size) {
  const scale = size / 64;
  
  // 身体
  ctx.fillStyle = '#2C3E50';
  ctx.beginPath();
  ctx.arc(32 * scale, 40 * scale, 16 * scale, 0, Math.PI * 2);
  ctx.fill();
  
  // 头
  ctx.fillStyle = '#2C3E50';
  ctx.beginPath();
  ctx.arc(32 * scale, 20 * scale, 12 * scale, 0, Math.PI * 2);
  ctx.fill();
  
  // 眼睛（智慧之光）
  ctx.fillStyle = '#FFFF00';
  ctx.beginPath();
  ctx.arc(28 * scale, 18 * scale, 3 * scale, 0, Math.PI * 2);
  ctx.fill();
  ctx.beginPath();
  ctx.arc(36 * scale, 18 * scale, 3 * scale, 0, Math.PI * 2);
  ctx.fill();
  
  // 喙
  ctx.fillStyle = '#FFD700';
  ctx.fillRect(32 * scale - 2 * scale, 24 * scale, 4 * scale, 6 * scale);
  
  // 翅膀
  ctx.fillStyle = '#1a1a1a';
  ctx.fillRect(16 * scale, 38 * scale, 8 * scale, 12 * scale);
  ctx.fillRect(40 * scale, 38 * scale, 8 * scale, 12 * scale);
}

function drawYoungReporter(ctx, size) {
  const scale = size / 64;
  
  // 头
  ctx.fillStyle = '#FFD4A3';
  ctx.fillRect(20 * scale, 10 * scale, 24 * scale, 22 * scale);
  
  // 长发
  ctx.fillStyle = '#2C2C54';
  ctx.fillRect(16 * scale, 8 * scale, 32 * scale, 16 * scale);
  
  // 皮夹克
  ctx.fillStyle = '#654321';
  ctx.fillRect(16 * scale, 32 * scale, 32 * scale, 24 * scale);
  
  // 腿
  ctx.fillStyle = '#2C2C54';
  ctx.fillRect(20 * scale, 54 * scale, 8 * scale, 10 * scale);
  ctx.fillRect(36 * scale, 54 * scale, 8 * scale, 10 * scale);
}

function drawMysteriousWoman(ctx, size) {
  const scale = size / 64;
  
  // 头
  ctx.fillStyle = '#FFD4A3';
  ctx.fillRect(20 * scale, 10 * scale, 24 * scale, 22 * scale);
  
  // 墨镜
  ctx.fillStyle = '#000000';
  ctx.fillRect(22 * scale, 16 * scale, 6 * scale, 6 * scale);
  ctx.fillRect(36 * scale, 16 * scale, 6 * scale, 6 * scale);
  
  // 紧身衣
  ctx.fillStyle = '#8B0000';
  ctx.fillRect(18 * scale, 32 * scale, 28 * scale, 28 * scale);
}

function drawOldWorker(ctx, size) {
  const scale = size / 64;
  
  // 头
  ctx.fillStyle = '#FFD4A3';
  ctx.fillRect(20 * scale, 12 * scale, 24 * scale, 20 * scale);
  
  // 花白胡须
  ctx.fillStyle = '#A9A9A9';
  ctx.fillRect(18 * scale, 28 * scale, 28 * scale, 6 * scale);
  
  // 工装
  ctx.fillStyle = '#8B4513';
  ctx.fillRect(16 * scale, 34 * scale, 32 * scale, 28 * scale);
}

function drawMadDoctor(ctx, size) {
  const scale = size / 64;
  
  // 头
  ctx.fillStyle = '#F5F5F5';
  ctx.fillRect(20 * scale, 10 * scale, 24 * scale, 24 * scale);
  
  // 白发
  ctx.fillStyle = '#FFFFFF';
  ctx.fillRect(16 * scale, 6 * scale, 32 * scale, 10 * scale);
  
  // 眼睛（冰冷）
  ctx.fillStyle = '#0000FF';
  ctx.fillRect(24 * scale, 18 * scale, 5 * scale, 5 * scale);
  ctx.fillRect(36 * scale, 18 * scale, 5 * scale, 5 * scale);
  
  // 白色实验服
  ctx.fillStyle = '#FFFFFF';
  ctx.fillRect(14 * scale, 34 * scale, 36 * scale, 28 * scale);
}

function drawSchoolGirl(ctx, size) {
  const scale = size / 64;
  
  // 头
  ctx.fillStyle = '#FFD4A3';
  ctx.fillRect(20 * scale, 10 * scale, 24 * scale, 22 * scale);
  
  // 长发
  ctx.fillStyle = '#8B4513';
  ctx.fillRect(16 * scale, 8 * scale, 32 * scale, 18 * scale);
  
  // 校服
  ctx.fillStyle = '#4169E1';
  ctx.fillRect(18 * scale, 32 * scale, 28 * scale, 20 * scale);
  
  // 裙子
  ctx.fillStyle = '#FF1493';
  ctx.fillRect(16 * scale, 52 * scale, 32 * scale, 12 * scale);
}

function drawShortHairFriend(ctx, size) {
  const scale = size / 64;
  
  // 头
  ctx.fillStyle = '#FFD4A3';
  ctx.fillRect(22 * scale, 10 * scale, 20 * scale, 20 * scale);
  
  // 短发
  ctx.fillStyle = '#DC143C';
  ctx.fillRect(18 * scale, 8 * scale, 28 * scale, 12 * scale);
  
  // 运动服
  ctx.fillStyle = '#00CED1';
  ctx.fillRect(18 * scale, 32 * scale, 28 * scale, 24 * scale);
}

function drawSchoolPrincipal(ctx, size) {
  const scale = size / 64;
  
  // 头
  ctx.fillStyle = '#FFD4A3';
  ctx.fillRect(20 * scale, 12 * scale, 24 * scale, 20 * scale);
  
  // 优雅黑袍
  ctx.fillStyle = '#1a1a2e';
  ctx.fillRect(14 * scale, 34 * scale, 36 * scale, 28 * scale);
  
  // 眼神智慧
  ctx.fillStyle = '#FFD700';
  ctx.beginPath();
  ctx.arc(28 * scale, 18 * scale, 2 * scale, 0, Math.PI * 2);
  ctx.fill();
  ctx.beginPath();
  ctx.arc(36 * scale, 18 * scale, 2 * scale, 0, Math.PI * 2);
  ctx.fill();
}

function drawTimeGuardian(ctx, size) {
  const scale = size / 64;
  
  // 半透明身体
  ctx.fillStyle = 'rgba(138, 43, 226, 0.5)';
  ctx.beginPath();
  ctx.arc(32 * scale, 32 * scale, 20 * scale, 0, Math.PI * 2);
  ctx.fill();
  
  // 闪闪发光的粒子
  ctx.fillStyle = '#00FFFF';
  for (let i = 0; i < 12; i++) {
    const angle = (i / 12) * Math.PI * 2;
    const x = 32 * scale + Math.cos(angle) * 24 * scale;
    const y = 32 * scale + Math.sin(angle) * 24 * scale;
    ctx.fillRect(x, y, 3 * scale, 3 * scale);
  }
}

function drawDefaultCharacter(ctx, size) {
  ctx.fillStyle = '#FFD4A3';
  ctx.fillRect(16, 10, 32, 30);
  ctx.fillStyle = '#8B4513';
  ctx.fillRect(18, 40, 28, 24);
}

// ===== 互动元素绘制函数 =====

function drawGlowingLeaf(ctx, size) {
  ctx.fillStyle = '#228B22';
  ctx.fillRect(8, 6, 16, 20);
  ctx.fillStyle = '#7FFFD4';
  ctx.fillRect(12, 10, 8, 8);
  ctx.fillStyle = '#00FFFF';
  ctx.fillRect(14, 12, 4, 4);
}

function drawBlueCrystal(ctx, size) {
  ctx.fillStyle = '#87CEEB';
  ctx.beginPath();
  ctx.moveTo(16, 4);
  ctx.lineTo(28, 12);
  ctx.lineTo(24, 28);
  ctx.lineTo(8, 24);
  ctx.lineTo(4, 12);
  ctx.closePath();
  ctx.fill();
  ctx.fillStyle = '#00BFFF';
  ctx.fillRect(12, 12, 8, 8);
}

function drawContractFragment(ctx, size) {
  ctx.fillStyle = '#FFD700';
  ctx.fillRect(6, 6, 20, 20);
  ctx.fillStyle = '#FFA500';
  ctx.fillRect(8, 8, 16, 16);
  ctx.fillStyle = '#FF6347';
  ctx.fillRect(12, 10, 8, 2);
  ctx.fillRect(12, 14, 8, 2);
  ctx.fillRect(12, 18, 8, 2);
}

function drawLetter(ctx, size) {
  ctx.fillStyle = '#F5F5F5';
  ctx.fillRect(6, 8, 20, 16);
  ctx.fillStyle = '#000000';
  ctx.fillRect(8, 10, 16, 2);
  ctx.fillRect(8, 14, 16, 2);
  ctx.fillRect(8, 18, 12, 2);
}

function drawPass(ctx, size) {
  ctx.fillStyle = '#DAA520';
  ctx.fillRect(4, 4, 24, 24);
  ctx.fillStyle = '#000000';
  ctx.fillRect(6, 6, 20, 20);
  ctx.fillStyle = '#FFD700';
  ctx.fillRect(10, 10, 12, 12);
}

function drawEvidenceFile(ctx, size) {
  ctx.fillStyle = '#8B0000';
  ctx.fillRect(6, 4, 20, 24);
  ctx.fillStyle = '#FFD700';
  ctx.fillRect(8, 6, 16, 8);
  ctx.fillStyle = '#FFFFFF';
  ctx.fillRect(8, 16, 16, 2);
  ctx.fillRect(8, 20, 16, 2);
}

function drawCherryPetal(ctx, size) {
  ctx.fillStyle = '#FF69B4';
  ctx.beginPath();
  ctx.arc(16, 16, 4, 0, Math.PI * 2);
  ctx.fill();
  ctx.fillStyle = '#FFB6C1';
  for (let i = 0; i < 4; i++) {
    const angle = (i / 4) * Math.PI * 2;
    const x = 16 + Math.cos(angle) * 8;
    const y = 16 + Math.sin(angle) * 8;
    ctx.beginPath();
    ctx.arc(x, y, 3, 0, Math.PI * 2);
    ctx.fill();
  }
}

function drawDiary(ctx, size) {
  ctx.fillStyle = '#8B4513';
  ctx.fillRect(6, 6, 20, 20);
  ctx.fillStyle = '#D2B48C';
  ctx.fillRect(8, 8, 16, 16);
  ctx.fillStyle = '#000000';
  ctx.fillRect(10, 10, 12, 12);
}

function drawLight(ctx, size) {
  ctx.fillStyle = '#FFFF00';
  ctx.beginPath();
  ctx.arc(16, 16, 6, 0, Math.PI * 2);
  ctx.fill();
  ctx.fillStyle = '#FFED4E';
  ctx.beginPath();
  ctx.arc(16, 16, 4, 0, Math.PI * 2);
  ctx.fill();
  ctx.fillStyle = '#FFFFFF';
  ctx.beginPath();
  ctx.arc(16, 16, 2, 0, Math.PI * 2);
  ctx.fill();
}

function drawDefaultElement(ctx, size) {
  ctx.fillStyle = '#FFD700';
  ctx.fillRect(6, 6, 20, 20);
}

// ===== 辅助绘制函数 =====

function drawPixelTriangle(ctx, x, y, width, height) {
  ctx.beginPath();
  ctx.moveTo(x, y);
  ctx.lineTo(x + width / 2, y - height);
  ctx.lineTo(x + width, y);
  ctx.closePath();
  ctx.fill();
}

function drawPixelTree(ctx, x, y, trunkWidth, totalHeight, color) {
  // 树干
  ctx.fillStyle = '#8B4513';
  ctx.fillRect(x - trunkWidth / 2, y, trunkWidth, totalHeight * 0.3);
  // 树冠
  ctx.fillStyle = color;
  drawPixelCircle(ctx, x, y - totalHeight * 0.2, totalHeight * 0.5);
}

function drawPixelCircle(ctx, x, y, radius) {
  for (let i = -radius; i <= radius; i++) {
    for (let j = -radius; j <= radius; j++) {
      if (i * i + j * j <= radius * radius) {
        ctx.fillRect(x + i, y + j, 1, 1);
      }
    }
  }
}

function drawPixelFlower(ctx, x, y, size) {
  ctx.fillRect(x - size, y, size * 2, size);
  ctx.fillRect(x, y - size, size, size * 2);
  ctx.fillStyle = '#FFD700';
  ctx.fillRect(x - size / 2, y - size / 2, size, size);
}

function drawPixelMushroom(ctx, x, y, size) {
  // 菌盖
  ctx.fillStyle = '#DC143C';
  drawPixelCircle(ctx, x, y - size, size * 1.5);
  // 菌柄
  ctx.fillStyle = '#F5DEB3';
  ctx.fillRect(x - size / 2, y - size, size, size * 2);
}

/**
 * 将Canvas转换为Base64数据URL
 * @param {HTMLCanvasElement} canvas
 * @returns {string} Data URL
 */
export function canvasToDataURL(canvas) {
  return canvas.toDataURL('image/png');
}

/**
 * 将Canvas转换为Blob
 * @param {HTMLCanvasElement} canvas
 * @returns {Promise<Blob>}
 */
export function canvasToBlob(canvas) {
  return new Promise((resolve) => {
    canvas.toBlob(resolve, 'image/png');
  });
}
