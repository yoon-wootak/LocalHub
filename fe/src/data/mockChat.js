/**
 * Mock 데이터 - 챗봇 개발용
 * 실제 FastAPI /api/chat 연동 전까지 사용되는 개발용 응답입니다.
 * 실제 API 연결 시 이 파일은 삭제되고 axios로 대체됩니다.
 */

export const chatSuggestions = [
  {
    id: 'suggest-1',
    label: '가족과 갈 만한 장소 추천',
    message: '가족과 갈 만한 장소를 추천해줘'
  },
  {
    id: 'suggest-2',
    label: '산책하기 좋은 곳',
    message: '산책하기 좋은 곳이 어디가 있어?'
  },
  {
    id: 'suggest-3',
    label: '비 오는 날 갈 만한 실내 장소',
    message: '비 오는 날 갈 만한 실내 장소를 알려줘'
  },
  {
    id: 'suggest-4',
    label: '지역 축제 정보',
    message: '구미에서 열리는 축제가 뭐가 있어?'
  }
]

/**
 * Mock 챗봇 응답 생성
 */
export const getMockChatResponse = async (message) => {
  const cleanMessage = message.trim()

  if (!cleanMessage) {
    throw new Error('빈 메시지는 전송할 수 없습니다.')
  }

  const lowerMessage = cleanMessage.toLowerCase()

  // 가족 관련
  if (lowerMessage.includes('가족') || lowerMessage.includes('아이')) {
    return {
      answer: '가족과 함께 즐길 수 있는 장소들을 추천드립니다.\n\n🌲 금오산 도립공원 - 케이블카나 쉬운 산책로로 온가족이 즐길 수 있습니다.\n🏞️ 동락공원 - 도심 속 산림공원으로 어린이들이 뛰어놀 수 있는 넓은 공간이 있습니다.\n🎭 구미문화예술회관 - 주말에 가족을 위한 공연과 전시가 자주 열립니다.\n\n최근 커뮤니티에서 가족 나들이 팁을 공유한 글들도 확인해보세요!',
      references: [
        { id: '1', type: 'place', title: '금오산 도립공원', path: '/places/1' },
        { id: '2', type: 'place', title: '동락공원', path: '/places/2' },
        { id: '3', type: 'place', title: '구미문화예술회관', path: '/places/3' }
      ]
    }
  }

  // 산책 관련
  if (lowerMessage.includes('산책')) {
    return {
      answer: '산책하기 좋은 구미의 장소들을 소개합니다.\n\n🌳 낙동강 둔치길 - 긴 산책로로 자연을 느끼며 걸을 수 있습니다. 계절마다 다른 경치를 감상할 수 있어요.\n🏞️ 동락공원 - 대나무 숲길 등 다양한 테마의 산책로가 있습니다.\n⛰️ 금오산 도립공원 - 정상까지의 여러 등산로 중 초보자도 갈 수 있는 코스가 있습니다.\n\n커뮤니티에서 더 자세한 산책 코스 정보를 얻을 수 있습니다.',
      references: [
        { id: '5', type: 'place', title: '낙동강 둔치길', path: '/places/5' },
        { id: '2', type: 'place', title: '동락공원', path: '/places/2' },
        { id: '1', type: 'place', title: '금오산 도립공원', path: '/places/1' }
      ]
    }
  }

  // 금오산 관련
  if (lowerMessage.includes('금오산')) {
    return {
      answer: '금오산 도립공원은 구미를 대표하는 관광지입니다.\n\n📍 위치: 경상북도 구미시 신동읍\n🏔️ 높이: 해발 976.5m\n⏱️ 운영: 24시간 개방\n💰 입장료: 무료\n\n정상에서는 구미 전경을 한눈에 볼 수 있으며, 사계절 내내 다양한 자연경관을 감상할 수 있습니다. 봄에는 철쭉, 가을에는 단풍이 아름답습니다.\n\n더 자세한 정보와 방문객 후기는 상세 페이지에서 확인할 수 있습니다.',
      references: [
        { id: '1', type: 'place', title: '금오산 도립공원 상세 정보', path: '/places/1' }
      ]
    }
  }

  // 실내 관련
  if (lowerMessage.includes('실내') || lowerMessage.includes('실내 장소')) {
    return {
      answer: '실내에서 즐길 수 있는 구미의 장소들입니다.\n\n🎭 구미문화예술회관 - 공연, 전시, 강좌 등 다양한 문화 프로그램을 제공합니다.\n🏛️ 한국 야금 박물관 - 구미 산업의 역사를 알 수 있는 박물관입니다.\n🛍️ 구미공단 쇼핑거리 - 다양한 상점에서 쇼핑을 즐길 수 있습니다.\n\n날씨와 관계없이 편하게 방문할 수 있는 곳들이에요.',
      references: [
        { id: '3', type: 'place', title: '구미문화예술회관', path: '/places/3' },
        { id: '4', type: 'place', title: '한국 야금 박물관', path: '/places/4' },
        { id: '6', type: 'place', title: '구미공단 쇼핑거리', path: '/places/6' }
      ]
    }
  }

  // 비 오는 날 관련
  if (lowerMessage.includes('비')) {
    return {
      answer: '비 오는 날씨에도 즐길 수 있는 실내 장소들을 추천합니다.\n\n🎭 구미문화예술회관 - 공연을 관람하며 문화생활을 즐길 수 있습니다.\n🏛️ 한국 야금 박물관 - 구미의 산업 역사를 배우며 시간을 보낼 수 있어요.\n🛍️ 쇼핑 시설 - 상점 방문과 쇼핑으로 오후를 즐겁게 보낼 수 있습니다.\n\n또한 커뮤니티에서 많은 주민들이 공유한 \"비 오는 날 가볼 만한 곳\" 정보도 확인해보세요!',
      references: [
        { id: '3', type: 'place', title: '구미문화예술회관', path: '/places/3' },
        { id: '4', type: 'place', title: '한국 야금 박물관', path: '/places/4' }
      ]
    }
  }

  // 축제 관련
  if (lowerMessage.includes('축제') || lowerMessage.includes('행사')) {
    return {
      answer: '구미의 주요 축제와 행사 정보입니다.\n\n🌸 봄 벚꽃 축제 - 3월 말~4월 초 구미의 여러 곳에서 벚꽃 축제가 열립니다.\n🎆 여름 축제 - 폭죽 축제 및 수상 문화 행사가 개최됩니다.\n🍂 가을 축제 - 지역 특산물 축제와 문화 행사가 개최돼요.\n❄️ 겨울 행사 - 연말 조명 축제와 새해 행사가 있습니다.\n\n정확한 일정은 커뮤니티에서 최신 정보를 확인해주세요!',
      references: [
        { id: 'post-6', type: 'post', title: '올봄 구미 벚꽃 축제 일정 안내', path: '/posts/6' }
      ]
    }
  }

  // 문화 관련
  if (lowerMessage.includes('문화') || lowerMessage.includes('공연') || lowerMessage.includes('전시')) {
    return {
      answer: '구미의 문화시설을 소개합니다.\n\n🎭 구미문화예술회관 - 지역 문화의 중심입니다.\n   • 공연: 음악회, 연극, 뮤지컬 등 다양한 무대 공연\n   • 전시: 정기적인 미술 전시와 사진 전시\n   • 강좌: 지역민을 위한 다양한 문화 교육 프로그램\n   • 전화: 054-450-1700\n\n최근 공연 후기와 전시 정보는 커뮤니티 게시글에서 확인할 수 있습니다.',
      references: [
        { id: '3', type: 'place', title: '구미문화예술회관', path: '/places/3' },
        { id: 'post-8', type: 'post', title: '구미문화예술회관 1월 공연 후기', path: '/posts/8' }
      ]
    }
  }

  // 동락공원 관련
  if (lowerMessage.includes('동락공원')) {
    return {
      answer: '동락공원은 구미의 중심 지역에 위치한 도시 공원입니다.\n\n📍 위치: 경상북도 구미시 동락로\n⏱️ 운영: 06:00 - 22:00\n💰 입장료: 무료\n\n✨ 특징:\n• 도심 속 산림공원으로 휴식처 역할\n• 산책로와 운동시설이 잘 갖춰져 있음\n• 대나무 숲길 등 테마별 산책로\n• 야간 조명으로 저녁 산책도 가능\n\n커뮤니티에서 주차 정보와 운영 정보에 대한 질문들을 확인할 수 있습니다.',
      references: [
        { id: '2', type: 'place', title: '동락공원', path: '/places/2' },
        { id: 'post-11', type: 'post', title: '동락공원 주차비가 얼마예요?', path: '/posts/11' }
      ]
    }
  }

  // 커뮤니티 관련
  if (lowerMessage.includes('커뮤니티') || lowerMessage.includes('게시글') || lowerMessage.includes('글')) {
    return {
      answer: 'LocalHub 커뮤니티는 지역 주민들이 정보를 나누는 익명 게시판입니다.\n\n📌 주요 카테고리:\n• 관광 - 추천 장소와 여행 정보\n• 맛집 - 구미의 맛있는 가게 소개\n• 생활 - 생활 정보와 팁\n• 질문 - 궁금한 점 묻기\n• 행사 - 지역 행사 정보\n• 자유 - 자유로운 이야기\n\n최근 활발한 주제들을 확인하고 직접 정보를 공유해보세요!\n회원가입 없이 익명으로 참여할 수 있습니다.',
      references: []
    }
  }

  // 기본 응답
  return {
    answer: '구미와 경북 지역의 관광지, 음식점, 축제, 생활 정보 등 다양한 질문에 답변드려요.\n\n💡 다음과 같은 질문을 해보세요:\n• \"가족과 갈 만한 장소는?\" \n• \"산책하기 좋은 곳을 추천해줘\"\n• \"실내에서 갈 수 있는 곳은?\"\n• \"금오산에 대해 알려줘\"\n• \"최근 축제 정보는?\"\n\n더 구체적인 정보를 원하신다면 추천 질문을 선택하거나 직접 물어봐주세요!',
    references: []
  }
}