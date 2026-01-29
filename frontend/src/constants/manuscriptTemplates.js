/**
 * 结构化原稿模板库
 * 包含三套风格各异的完整游戏原稿模板
 */

export const MANUSCRIPT_TEMPLATES = [
  {
    id: 'template_1',
    name: '森林的守护者',
    style: '温暖冒险',
    description: '一个关于守护森林的治愈系冒险故事',
    data: {
      storyTitle: '森林的守护者',
      selectedEmotionOption: 'warm',
      emotionalTone: 'warm',
      customEmotionalTone: '',
      storyOutline: '在一个被遗忘的古老森林中，曾经有一位可以与自然交流的守护者。她在一场灾难中失去了力量，森林开始枯萎。主角作为新一代守护者，需要穿过森林的各个区域，恢复与灵兽的契约，最终拯救这片古老的生命源地。故事在主角与森林灵兽的情感互动中展开，通过完成自然任务逐步解锁森林的记忆，最终发现守护者与森林的真正连接。',
      gameBackground: '魔法古老森林，风格为清新治愈的像素风。包括翠绿的树林、闪闪发光的精灵草地、古老的遗迹神殿、蕴含魔力的水晶湖泊。四季变化的场景设计，从春天的复苏到冬天的沉寂。',
      missions: [
        {
          name: '寻找森林的第一盏灯',
          triggerCondition: '进入森林边缘区域',
          completionCondition: '找到第一个灵兽石碑，解读其中的信息',
          storyProgression: '了解到曾经的守护者和第一只守护灵兽的故事'
        },
        {
          name: '修复森林心脏的三个水晶',
          triggerCondition: '获得森林长者的指引',
          completionCondition: '收集三个被污染的水晶并在圣泉净化',
          storyProgression: '森林开始逐步恢复生机，解锁新的可达区域'
        },
        {
          name: '与灵兽达成新的契约',
          triggerCondition: '收集足够的灵兽信息',
          completionCondition: '在月圆之夜与四只灵兽进行仪式对话',
          storyProgression: '获得灵兽之力，成为新时代的森林守护者'
        },
        {
          name: '守护森林迎接新生',
          triggerCondition: '完成与所有灵兽的契约',
          completionCondition: '参与森林复苏的最终庆典',
          storyProgression: '故事圆满结束，森林恢复昔日光彩'
        }
      ],
      characters: [
        {
          name: '月影',
          personality: '温柔、博学、充满母爱般的关怀',
          appearance: '银白长发的女性精灵，穿着清晨的雾气般飘逸的衣裳，额头有月亮纹样',
          speechStyle: '温柔而富有诗意，经常用自然比喻来表达思想'
        },
        {
          name: '石谷',
          personality: '沉稳、坚毅、略显固执，对传统充满尊重',
          appearance: '岩石般厚实的身体，胡须花白的老地精，穿着古老的石器工艺图案',
          speechStyle: '低沉而缓慢，说话充满权威和历史感'
        },
        {
          name: '火狐',
          personality: '活泼、调皮、充满好奇心，但心地善良',
          appearance: '橙红色毛发的小狐灵，尾巴闪闪发光，眼睛炯炯有神',
          speechStyle: '活泼俏皮，经常用拟声词，充满少女感'
        },
        {
          name: '古董',
          personality: '神秘、智慧、高冷但一旦信任就无比忠诚',
          appearance: '深紫色羽毛的巨型乌鸦，眼睛闪烁着古老的智慧之光',
          speechStyle: '精炼而深邃，每句话都值得深思'
        }
      ]
    }
  },
  {
    id: 'template_2',
    name: '城市的秘密',
    style: '悬疑科幻',
    description: '一个关于发现隐藏秘密的悬疑故事',
    data: {
      storyTitle: '城市的秘密',
      selectedEmotionOption: 'suspense',
      emotionalTone: 'suspense',
      customEmotionalTone: '',
      storyOutline: '在一个赛博朋克风格的未来城市中，主角是一位记者。他发现了一系列诡异的失踪事件都指向同一个地点——城市地下的秘密实验室。通过收集线索、追踪证据、与线人接头，主角逐步揭开城市统治者隐瞒的真相。故事充满转折，玩家的选择会影响故事走向，是揭露真相还是被真相吞没取决于你的每一个决定。',
      gameBackground: '赛博朋克未来城市，夜幕下霓虹灯闪烁的街道、高耸的摩天大楼、布满监控摄像头的小巷、神秘的地下工作室。冷色调的像素风设计，充满压抑和神秘的氛围。',
      missions: [
        {
          name: '第一条线索',
          triggerCondition: '接到神秘来电',
          completionCondition: '前往指定地点收集第一份线索文件',
          storyProgression: '发现失踪案件的蛛丝马迹'
        },
        {
          name: '审讯线人',
          triggerCondition: '获得线人的位置信息',
          completionCondition: '在城市各处找到三位线人进行对话',
          storyProgression: '了解到城市的更多黑暗秘密'
        },
        {
          name: '潜入禁地',
          triggerCondition: '收集足够的安全通行证',
          completionCondition: '绕过安全防护系统，进入地下实验室',
          storyProgression: '发现真实的实验内容，面临道德抉择'
        },
        {
          name: '最终对决',
          triggerCondition: '掌握核心证据',
          completionCondition: '与黑手党首脑进行最终摊牌',
          storyProgression: '故事走向由玩家的选择决定'
        }
      ],
      characters: [
        {
          name: '雷克斯',
          personality: '聪慧、执着、富有正义感，但有些固执己见',
          appearance: '留着长发的年轻记者，穿着破旧的皮夹克，眼神中充满不信任',
          speechStyle: '快速而尖锐，经常问关键问题，充满记者的职业素养'
        },
        {
          name: '夜莺',
          personality: '神秘、聪敏、行动派，动机不明确',
          appearance: '戴着墨镜的神秘女性，穿着紧身衣，在阴影中隐现',
          speechStyle: '简洁而隐晦，言语中充满暗示'
        },
        {
          name: '老赵',
          personality: '沧桑、热心肠、知识渊博的地下工作者',
          appearance: '年迈的中年男性，一只眼睛被机械替换，穿着古旧的工装',
          speechStyle: '江湖气息浓厚，说话充满黑话和隐喻'
        },
        {
          name: '博士',
          personality: '疯狂、天才、缺乏道德底线，对权力执着',
          appearance: '白发苍苍的老人，穿着整洁的白色实验服，目光冰冷'
        }
      ]
    }
  },
  {
    id: 'template_3',
    name: '光阴的故事',
    style: '浪漫文艺',
    description: '一个关于青春和回忆的文艺爱情故事',
    data: {
      storyTitle: '光阴的故事',
      selectedEmotionOption: 'romantic',
      emotionalTone: 'romantic',
      customEmotionalTone: '',
      storyOutline: '故事发生在一所魔法学院的校园中。主角在整理学校的旧相册时，发现了一张神秘的照片——一个穿着校服的女孩站在校园的某个角落。通过探索校园的各个场景，主角逐渐回忆起与她的点滴故事。每个场景都对应一段回忆，通过完成一系列温暖而浪漫的任务，最终两人的故事在校园的最高塔前达到高潮。游戏充满光影和音乐的交织，每个选择都影响着故事的浪漫程度。',
      gameBackground: '魔法学院校园，采用温暖清新的像素风。包括教堂般的宏伟校舍、开满鲜花的庭院、充满书籍的图书馆、漫天星辰的天台、樱花飘落的小径。整个画面色调柔和，充满光影的诗意。',
      missions: [
        {
          name: '寻找回忆的碎片',
          triggerCondition: '发现神秘的旧照片',
          completionCondition: '在校园各地收集与女孩相关的物品',
          storyProgression: '开始回忆一段尘封的青春'
        },
        {
          name: '重游校园的每个角落',
          triggerCondition: '掌握足够的回忆碎片',
          completionCondition: '访问学院的五个标志性地点，触发回忆场景',
          storyProgression: '每个地点都带来一段美好而酸涩的回忆'
        },
        {
          name: '勇气的决定',
          triggerCondition: '所有回忆都已解锁',
          completionCondition: '选择是否去天台与女孩相见',
          storyProgression: '人生的转折点到来'
        },
        {
          name: '光阴见证',
          triggerCondition: '做出最终选择',
          completionCondition: '在校园最高塔前经历故事的结局',
          storyProgression: '一个属于两个人的永恒时刻'
        }
      ],
      characters: [
        {
          name: '君',
          personality: '温柔、细心、略显内向但充满温暖',
          appearance: '穿着魔法学院校服的女孩，长发披肩，眼睛闪闪发光',
          speechStyle: '柔和而温暖，说话时经常微笑，充满女性的温柔'
        },
        {
          name: '林岚',
          personality: '友善、活泼、充满正义感，是主角最好的朋友',
          appearance: '短发女孩，穿着运动版校服，脸上始终带着笑容',
          speechStyle: '明快爽朗，经常鼓励主角，充满青春气息'
        },
        {
          name: '校长',
          personality: '智慧、温暖、对学生充满期许',
          appearance: '年长的女性，穿着优雅的黑袍，眼睛充满智慧的光芒',
          speechStyle: '有教养而富有哲理，如同长辈的教诲'
        },
        {
          name: '时间守护者',
          personality: '神秘、古老、掌控时间的魔法生物',
          appearance: '半透明的幽灵状生物，身上闪闪发光的粒子不断流动',
          speechStyle: '古老而低沉，说话充满超越时间的智慧'
        }
      ]
    }
  }
];

/**
 * 获取随机模板
 */
export const getRandomTemplate = () => {
  const randomIndex = Math.floor(Math.random() * MANUSCRIPT_TEMPLATES.length);
  return MANUSCRIPT_TEMPLATES[randomIndex];
};

/**
 * 获取指定ID的模板
 */
export const getTemplateById = (id) => {
  return MANUSCRIPT_TEMPLATES.find(template => template.id === id);
};

/**
 * 获取所有模板列表
 */
export const getAllTemplates = () => {
  return MANUSCRIPT_TEMPLATES.map(template => ({
    id: template.id,
    name: template.name,
    style: template.style,
    description: template.description
  }));
};
