/**
 * 游戏预设数据库
 * 为三套原稿模板生成对应的完整游戏数据
 * 用于可视化编辑和项目预览
 */

import { injectAssets } from './assetConfig'

export const GAME_PRESETS = [
  {
    id: 'preset_1',
    templateId: 'template_1',
    name: '森林的守护者',
    gameName: '森林的守护者',
    emotionalTone: 'warm',
    style: 'pixel_art',
    gameData: {
      gameId: 'game_template_1',
      gameName: '森林的守护者',
      emotionalTone: 'warm',
      style: 'pixel_art',
      scenes: [
        {
          id: 'scene_1',
          name: '翠绿森林入口',
          backgroundDescription: '一片生机勃勃的魔法森林，翠绿的树木耸立，光线透过树叶洒下来形成斑驳的阴影。地上长满了闪闪发光的精灵草，空气中弥漫着魔法的气息。',
          interactiveElements: [
            {
              type: 'npc',
              name: '月影',
              position: [150, 120],
              description: '温柔的精灵长者',
              dialogue: ['欢迎来到古老的森林...', '我曾是这片森林的守护者，但我的力量已经逐渐消褪了。', '你能帮助我恢复这片森林吗？']
            },
            {
              type: 'item',
              name: '发光的树叶',
              position: [250, 180],
              description: '这是森林活力的象征',
              dialogue: ['获得了发光的树叶！']
            }
          ],
          transitions: [
            { targetScene: 'scene_2', direction: 'right', condition: '靠近右边界' }
          ]
        },
        {
          id: 'scene_2',
          name: '精灵草地',
          backgroundDescription: '广阔的草地上长满了闪闪发光的精灵草，每一株都在散发着柔和的蓝色光芒。中央有一块古老的石头，上面刻满了神秘的纹样。',
          interactiveElements: [
            {
              type: 'npc',
              name: '火狐',
              position: [200, 150],
              description: '活泼的小狐灵',
              dialogue: ['哇！你来了！', '我之前在这里丢失了一样重要的东西...', '你能帮我找到它吗？']
            },
            {
              type: 'item',
              name: '青色水晶',
              position: [300, 200],
              description: '森林心脏的一部分，需要净化',
              dialogue: ['获得了青色水晶！']
            }
          ],
          transitions: [
            { targetScene: 'scene_1', direction: 'left', condition: '靠近左边界' },
            { targetScene: 'scene_3', direction: 'down', condition: '靠近下边界' }
          ]
        },
        {
          id: 'scene_3',
          name: '神圣泉水',
          backgroundDescription: '一汪清澈的水晶般的泉水，周围环绕着古老的石头祭坛。泉水散发着柔和的白色光芒，仿佛拥有净化一切的力量。',
          interactiveElements: [
            {
              type: 'npc',
              name: '石谷',
              position: [180, 140],
              description: '沉稳的地精智者',
              dialogue: ['这是我们祖先建立的神圣泉水。', '据说它能净化被污染的魔法结晶。', '如果你带来被污染的结晶，我可以帮助净化它们。']
            }
          ],
          transitions: [
            { targetScene: 'scene_2', direction: 'up', condition: '靠近上边界' },
            { targetScene: 'scene_4', direction: 'right', condition: '靠近右边界' }
          ]
        },
        {
          id: 'scene_4',
          name: '古老遗迹',
          backgroundDescription: '破旧的古代建筑遗迹，被藤蔓和蘑菇覆盖。石柱上刻满了历史的痕迹，这里弥漫着久远的时光气息。',
          interactiveElements: [
            {
              type: 'npc',
              name: '古董',
              position: [220, 160],
              description: '神秘的乌鸦贤者',
              dialogue: ['我见证了这个森林的兴衰。', '四只灵兽的契约碎片正在这片古迹中等待...', '只有找到它们，你才能成为真正的守护者。']
            },
            {
              type: 'item',
              name: '灵兽契约碎片',
              position: [320, 200],
              description: '与灵兽沟通的关键',
              dialogue: ['获得了灵兽契约碎片！']
            }
          ],
          transitions: [
            { targetScene: 'scene_3', direction: 'left', condition: '靠近左边界' }
          ]
        }
      ],
      characters: [
        {
          id: 'char_1',
          name: '月影',
          appearance: '银白长发的女性精灵，穿着清晨的雾气般飘逸的衣裳，额头有月亮纹样',
          personality: '温柔、博学、充满母爱般的关怀',
          initialPosition: 'scene_1',
          dialogues: [
            '欢迎来到古老的森林...',
            '我曾是这片森林的守护者，但我的力量已经逐渐消褪了。',
            '你能帮助我恢复这片森林吗？',
            '感谢你的帮助，我能感受到森林正在复苏...'
          ]
        },
        {
          id: 'char_2',
          name: '火狐',
          appearance: '橙红色毛发的小狐灵，尾巴闪闪发光，眼睛炯炯有神',
          personality: '活泼、调皮、充满好奇心，但心地善良',
          initialPosition: 'scene_2',
          dialogues: [
            '哇！你来了！',
            '我之前在这里丢失了一样重要的东西...',
            '你能帮我找到它吗？',
            '谢谢你帮我找回来了！我们以后会经常见面的！'
          ]
        },
        {
          id: 'char_3',
          name: '石谷',
          appearance: '岩石般厚实的身体，胡须花白的老地精，穿着古老的石器工艺图案',
          personality: '沉稳、坚毅、略显固执，对传统充满尊重',
          initialPosition: 'scene_3',
          dialogues: [
            '这是我们祖先建立的神圣泉水。',
            '据说它能净化被污染的魔法结晶。',
            '如果你带来被污染的结晶，我可以帮助净化它们。',
            '很好，我感受到了古老的守护者之力在你身上苏醒。'
          ]
        },
        {
          id: 'char_4',
          name: '古董',
          appearance: '深紫色羽毛的巨型乌鸦，眼睛闪烁着古老的智慧之光',
          personality: '神秘、智慧、高冷但一旦信任就无比忠诚',
          initialPosition: 'scene_4',
          dialogues: [
            '我见证了这个森林的兴衰。',
            '四只灵兽的契约碎片正在这片古迹中等待...',
            '只有找到它们，你才能成为真正的守护者。',
            '你已经准备好了。让我见证你与灵兽的新契约。'
          ]
        }
      ],
      missions: [
        {
          id: 'mission_1',
          name: '寻找森林的第一盏灯',
          triggerScene: 'scene_1',
          triggerCondition: '与月影对话',
          completionCondition: '收集发光的树叶',
          dialogueContent: '我能感受到森林深处有一些东西在呼唤...',
          reward: { xp: 100, items: ['发光的树叶'] },
          nextMissionId: 'mission_2'
        },
        {
          id: 'mission_2',
          name: '修复森林心脏的三个水晶',
          triggerScene: 'scene_2',
          triggerCondition: '收集到足够的结晶',
          completionCondition: '在泉水中净化所有结晶',
          dialogueContent: '森林的心脏在跳动...这是生命的声音！',
          reward: { xp: 200, items: ['净化的水晶'] },
          nextMissionId: 'mission_3'
        },
        {
          id: 'mission_3',
          name: '与灵兽达成新的契约',
          triggerScene: 'scene_4',
          triggerCondition: '集齐所有契约碎片',
          completionCondition: '在月圆之夜进行契约仪式',
          dialogueContent: '灵兽们在等待...一个新的时代即将开始！',
          reward: { xp: 300, items: ['灵兽之力'] },
          nextMissionId: 'mission_4'
        },
        {
          id: 'mission_4',
          name: '守护森林迎接新生',
          triggerScene: 'scene_1',
          triggerCondition: '完成所有灵兽契约',
          completionCondition: '参与森林复苏的最终庆典',
          dialogueContent: '森林已经复苏...感谢你，新的守护者！',
          reward: { xp: 500, items: ['守护者的王冠'] },
          nextMissionId: null
        }
      ],
      interactionRules: {
        movement: {
          up: '向上移动',
          down: '向下移动',
          left: '向左移动',
          right: '向右移动'
        },
        dialogueTrigger: {
          distance: 30,
          key: 'SPACE'
        },
        itemInteraction: {
          distance: 20,
          key: 'E'
        }
      }
    }
  },
  {
    id: 'preset_2',
    templateId: 'template_2',
    name: '城市的秘密',
    gameName: '城市的秘密',
    emotionalTone: 'suspense',
    style: 'pixel_art',
    gameData: {
      gameId: 'game_template_2',
      gameName: '城市的秘密',
      emotionalTone: 'suspense',
      style: 'pixel_art',
      scenes: [
        {
          id: 'scene_1',
          name: '记者办公室',
          backgroundDescription: '破旧的记者办公室，到处是纸张和线索板。窗外是城市的霓虹灯。一通神秘的来电打破了夜晚的寂静。',
          interactiveElements: [
            {
              type: 'npc',
              name: '来电者',
              position: [180, 140],
              description: '神秘的声音',
              dialogue: ['有人在追踪我...', '失踪案的真相就在地下...', '小心，他们在监控每个地方...']
            },
            {
              type: 'item',
              name: '神秘信件',
              position: [250, 160],
              description: '第一条线索',
              dialogue: ['获得了线索！']
            }
          ],
          transitions: [
            { targetScene: 'scene_2', direction: 'right', condition: '获得线索后前进' }
          ]
        },
        {
          id: 'scene_2',
          name: '暗夜街道',
          backgroundDescription: '城市的阴暗角落，霓虹灯闪烁，到处是监控摄像头。一个身影在阴影中移动。',
          interactiveElements: [
            {
              type: 'npc',
              name: '神秘女性',
              position: [200, 150],
              description: '夜莺',
              dialogue: ['你就是那个记者？', '我可以帮助你...但要付出代价。', '地下有你需要知道的真相...']
            }
          ],
          transitions: [
            { targetScene: 'scene_1', direction: 'left', condition: '返回' },
            { targetScene: 'scene_3', direction: 'down', condition: '前往地下' }
          ]
        },
        {
          id: 'scene_3',
          name: '地下停车场',
          backgroundDescription: '昏暗的地下停车场，混凝土墙壁，到处是油渍。警报灯闪烁。',
          interactiveElements: [
            {
              type: 'npc',
              name: '线人老赵',
              position: [220, 160],
              description: '沧桑的地下工作者',
              dialogue: ['这地方不安全...', '它们在地下进行非法实验。', '如果你要进去，你需要这个...']
            },
            {
              type: 'item',
              name: '通行证',
              position: [300, 180],
              description: '进入实验室的钥匙',
              dialogue: ['获得了通行证！']
            }
          ],
          transitions: [
            { targetScene: 'scene_2', direction: 'up', condition: '返回' },
            { targetScene: 'scene_4', direction: 'down', condition: '使用通行证进入' }
          ]
        },
        {
          id: 'scene_4',
          name: '秘密实验室',
          backgroundDescription: '高科技的地下实验室，闪烁的设备、液体管道、巨大的玻璃舱。空气中弥漫着诡异的气氛。',
          interactiveElements: [
            {
              type: 'npc',
              name: '疯狂博士',
              position: [240, 140],
              description: '实验的主使者',
              dialogue: ['欢迎来到真相所在...', '你终于来了，你会看到我们的伟大计划...', '但你不能活着离开这里。']
            },
            {
              type: 'item',
              name: '证据文件',
              position: [280, 200],
              description: '隐藏的真相',
              dialogue: ['获得了决定性证据！']
            }
          ],
          transitions: [
            { targetScene: 'scene_3', direction: 'up', condition: '逃脱' }
          ]
        }
      ],
      characters: [
        {
          id: 'char_1',
          name: '雷克斯',
          appearance: '留着长发的年轻记者，穿着破旧的皮夹克，眼神中充满不信任',
          personality: '聪慧、执着、富有正义感，但有些固执己见',
          initialPosition: 'scene_1',
          dialogues: [
            '又是一个诡异的案件...',
            '这一次，我一定要揭露真相！',
            '无论多危险，无论要付出什么代价。'
          ]
        },
        {
          id: 'char_2',
          name: '夜莺',
          appearance: '戴着墨镜的神秘女性，穿着紧身衣，在阴影中隐现',
          personality: '神秘、聪敏、行动派，动机不明确',
          initialPosition: 'scene_2',
          dialogues: [
            '我们有共同的敌人。',
            '相信我，或者死亡。',
            '选择权在你手中。'
          ]
        },
        {
          id: 'char_3',
          name: '老赵',
          appearance: '年迈的中年男性，一只眼睛被机械替换，穿着古旧的工装',
          personality: '沧桑、热心肠、知识渊博的地下工作者',
          initialPosition: 'scene_3',
          dialogues: [
            '我在这下面工作了20年...',
            '我看到过太多不该看到的东西...',
            '希望你能活着出去。'
          ]
        },
        {
          id: 'char_4',
          name: '博士',
          appearance: '白发苍苍的老人，穿着整洁的白色实验服，目光冰冷',
          personality: '疯狂、天才、缺乏道德底线，对权力执着',
          initialPosition: 'scene_4',
          dialogues: [
            '科学没有道德...只有结果！',
            '你不该来这里...',
            '现在，你将成为我们计划的一部分。'
          ]
        }
      ],
      missions: [
        {
          id: 'mission_1',
          name: '第一条线索',
          triggerScene: 'scene_1',
          triggerCondition: '接到来电',
          completionCondition: '收集第一份线索文件',
          dialogueContent: '有人在暗中指引我...这是什么阴谋？',
          reward: { xp: 100, items: ['线索1'] },
          nextMissionId: 'mission_2'
        },
        {
          id: 'mission_2',
          name: '审讯线人',
          triggerScene: 'scene_2',
          triggerCondition: '获得线索',
          completionCondition: '与三位线人对话',
          dialogueContent: '越来越多的真相浮现...这远比我想象的更黑暗。',
          reward: { xp: 200, items: ['线人名单'] },
          nextMissionId: 'mission_3'
        },
        {
          id: 'mission_3',
          name: '潜入禁地',
          triggerScene: 'scene_3',
          triggerCondition: '获得通行证',
          completionCondition: '进入地下实验室',
          dialogueContent: '事实真相就在眼前...但我将面对什么？',
          reward: { xp: 300, items: ['通行证'] },
          nextMissionId: 'mission_4'
        },
        {
          id: 'mission_4',
          name: '最终对决',
          triggerScene: 'scene_4',
          triggerCondition: '潜入实验室',
          completionCondition: '获得决定性证据',
          dialogueContent: '这是最后的时刻...我必须做出选择。',
          reward: { xp: 500, items: ['证据'] },
          nextMissionId: null
        }
      ],
      interactionRules: {
        movement: {
          up: '向上移动',
          down: '向下移动',
          left: '向左移动',
          right: '向右移动'
        },
        dialogueTrigger: {
          distance: 30,
          key: 'SPACE'
        },
        itemInteraction: {
          distance: 20,
          key: 'E'
        }
      }
    }
  },
  {
    id: 'preset_3',
    templateId: 'template_3',
    name: '光阴的故事',
    gameName: '光阴的故事',
    emotionalTone: 'romantic',
    style: 'pixel_art',
    gameData: {
      gameId: 'game_template_3',
      gameName: '光阴的故事',
      emotionalTone: 'romantic',
      style: 'pixel_art',
      scenes: [
        {
          id: 'scene_1',
          name: '学院主堂',
          backgroundDescription: '雄伟的教堂般建筑，彩色玻璃窗洒下温暖的光。古老的木质楼梯通往更高的地方。墙上挂满了历届学生的照片。',
          interactiveElements: [
            {
              type: 'npc',
              name: '林岚',
              position: [150, 120],
              description: '活泼的闺蜜',
              dialogue: ['你终于来了！', '你还记得那张旧照片吗？', '我一直以为你忘记了她...']
            },
            {
              type: 'item',
              name: '神秘照片',
              position: [250, 180],
              description: '尘封的青春记忆',
              dialogue: ['获得了照片！尘封的回忆开始苏醒...']
            }
          ],
          transitions: [
            { targetScene: 'scene_2', direction: 'right', condition: '前往庭院' },
            { targetScene: 'scene_3', direction: 'down', condition: '前往图书馆' }
          ]
        },
        {
          id: 'scene_2',
          name: '樱花庭院',
          backgroundDescription: '樱花纷纷扬扬地飘落，一条小径通过花瓣铺成的地面。一棵古老的樱花树在庭院中央。微风中传来温暖的气息。',
          interactiveElements: [
            {
              type: 'npc',
              name: '君',
              position: [200, 150],
              description: '温柔内向的女主',
              dialogue: ['你...还记得吗？', '那时候...我们在这里有过美好的时光。', '你说要永远守护我...']
            },
            {
              type: 'item',
              name: '樱花花瓣',
              position: [280, 200],
              description: '最珍贵的回忆象征',
              dialogue: ['这些花瓣就像时光的碎片...']
            }
          ],
          transitions: [
            { targetScene: 'scene_1', direction: 'left', condition: '返回' },
            { targetScene: 'scene_5', direction: 'up', condition: '前往天台' }
          ]
        },
        {
          id: 'scene_3',
          name: '古老图书馆',
          backgroundDescription: '充满书籍的宽敞空间，阳光透过高大的窗户洒进来。书架延伸到天花板，弥漫着知识和时光的气息。',
          interactiveElements: [
            {
              type: 'npc',
              name: '校长',
              position: [220, 160],
              description: '智慧的长者',
              dialogue: ['年轻人...', '你回来了。', '有些人，有些感情，值得用一生去等待。']
            },
            {
              type: 'item',
              name: '青春日记',
              position: [300, 200],
              description: '关于她的回忆',
              dialogue: ['翻开日记...所有的感情如潮水般涌来。']
            }
          ],
          transitions: [
            { targetScene: 'scene_1', direction: 'up', condition: '返回' },
            { targetScene: 'scene_4', direction: 'right', condition: '前往小径' }
          ]
        },
        {
          id: 'scene_4',
          name: '月光小径',
          backgroundDescription: '被月光照亮的樱花小径，两侧是盛开的花朵。一条通往天台的台阶，用星光标记。空气中充满了浪漫的气息。',
          interactiveElements: [
            {
              type: 'npc',
              name: '时间守护者',
              position: [240, 140],
              description: '掌控时间的魔法生物',
              dialogue: ['时间总是在流逝...', '但某些时刻...永远值得被珍藏。', '你准备好面对你的选择了吗？']
            }
          ],
          transitions: [
            { targetScene: 'scene_3', direction: 'left', condition: '返回' },
            { targetScene: 'scene_5', direction: 'up', condition: '前往天台' }
          ]
        },
        {
          id: 'scene_5',
          name: '校园最高塔',
          backgroundDescription: '星辰闪烁的夜空，两个人站在塔顶。月光洒下，照亮了两个身影。风中传来温暖的声音。这是永恒的时刻。',
          interactiveElements: [
            {
              type: 'npc',
              name: '君',
              position: [200, 120],
              description: '等待中的她',
              dialogue: ['你...真的来了。', '我等你很久了...', '这次，你愿意留下吗？']
            }
          ],
          transitions: [
            { targetScene: 'scene_2', direction: 'down', condition: '返回' },
            { targetScene: 'scene_4', direction: 'down', condition: '返回' }
          ]
        }
      ],
      characters: [
        {
          id: 'char_1',
          name: '君',
          appearance: '穿着魔法学院校服的女孩，长发披肩，眼睛闪闪发光',
          personality: '温柔、细心、略显内向但充满温暖',
          initialPosition: 'scene_2',
          dialogues: [
            '你...还记得吗？',
            '那时候...我们在这里有过美好的时光。',
            '你说要永远守护我...',
            '现在...我就在这里等你。'
          ]
        },
        {
          id: 'char_2',
          name: '林岚',
          appearance: '短发女孩，穿着运动版校服，脸上始终带着笑容',
          personality: '友善、活泼、充满正义感，是主角最好的朋友',
          initialPosition: 'scene_1',
          dialogues: [
            '你终于来了！',
            '你还记得那张旧照片吗？',
            '我一直以为你忘记了她...',
            '去吧，去见她，去说出你的心里话！'
          ]
        },
        {
          id: 'char_3',
          name: '校长',
          appearance: '年长的女性，穿着优雅的黑袍，眼睛充满智慧的光芒',
          personality: '智慧、温暖、对学生充满期许',
          initialPosition: 'scene_3',
          dialogues: [
            '年轻人...',
            '你回来了。',
            '有些人，有些感情，值得用一生去等待。',
            '青春稍纵即逝，但爱是永恒的。'
          ]
        },
        {
          id: 'char_4',
          name: '时间守护者',
          appearance: '半透明的幽灵状生物，身上闪闪发光的粒子不断流动',
          personality: '神秘、古老、掌控时间的魔法生物',
          initialPosition: 'scene_4',
          dialogues: [
            '时间总是在流逝...',
            '但某些时刻...永远值得被珍藏。',
            '你准备好面对你的选择了吗？',
            '在我的见证下，请说出你的誓言。'
          ]
        }
      ],
      missions: [
        {
          id: 'mission_1',
          name: '寻找回忆的碎片',
          triggerScene: 'scene_1',
          triggerCondition: '发现神秘的旧照片',
          completionCondition: '在校园各地收集物品',
          dialogueContent: '尘封的青春记忆开始苏醒...',
          reward: { xp: 100, items: ['回忆碎片'] },
          nextMissionId: 'mission_2'
        },
        {
          id: 'mission_2',
          name: '重游校园的每个角落',
          triggerScene: 'scene_2',
          triggerCondition: '掌握足够的回忆',
          completionCondition: '访问学院的标志性地点',
          dialogueContent: '每个地点都带来一段美好而酸涩的回忆...',
          reward: { xp: 200, items: ['青春记忆'] },
          nextMissionId: 'mission_3'
        },
        {
          id: 'mission_3',
          name: '勇气的决定',
          triggerScene: 'scene_4',
          triggerCondition: '所有回忆都已解锁',
          completionCondition: '选择是否前往天台',
          dialogueContent: '人生的转折点到来了...',
          reward: { xp: 300, items: ['勇气的心'] },
          nextMissionId: 'mission_4'
        },
        {
          id: 'mission_4',
          name: '光阴见证',
          triggerScene: 'scene_5',
          triggerCondition: '做出最终选择',
          completionCondition: '在校园最高塔前完成故事',
          dialogueContent: '这是一个属于两个人的永恒时刻...',
          reward: { xp: 500, items: ['永恒的爱'] },
          nextMissionId: null
        }
      ],
      interactionRules: {
        movement: {
          up: '向上移动',
          down: '向下移动',
          left: '向左移动',
          right: '向右移动'
        },
        dialogueTrigger: {
          distance: 30,
          key: 'SPACE'
        },
        itemInteraction: {
          distance: 20,
          key: 'E'
        }
      }
    }
  }
];

/**
 * 根据模板ID获取预设游戏数据壶注入素材
 */
export const getPresetByTemplateId = (templateId) => {
  const preset = GAME_PRESETS.find(preset => preset.templateId === templateId);
  if (preset) {
    return {
      ...preset,
      gameData: injectAssets(preset.gameData)
    };
  }
  return null;
};

/**
 * 获取随机预设注入素材
 */
export const getRandomPreset = () => {
  const randomIndex = Math.floor(Math.random() * GAME_PRESETS.length);
  const preset = GAME_PRESETS[randomIndex];
  return {
    ...preset,
    gameData: injectAssets(preset.gameData)
  };
};

/**
 * 获取所有预设列表
 */
export const getAllPresets = () => {
  return GAME_PRESETS.map(preset => ({
    id: preset.id,
    name: preset.name,
    emotionalTone: preset.emotionalTone
  }));
};
