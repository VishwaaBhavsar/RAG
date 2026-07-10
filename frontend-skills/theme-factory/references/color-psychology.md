# Color Psychology Framework

Brand archetypes and emotional associations for autonomous color selection.

## Brand Archetypes & Colors

### The Innocent
**Traits**: Optimistic, honest, simple, trustworthy
**Colors**: Soft blue, white, yellow, light green
**Avoid**: Dark colors, complex palettes
**Best For**: Health, organic products, children's brands

### The Explorer
**Traits**: Independent, adventurous, authentic
**Colors**: Earth tones, forest green, sky blue, tan
**Avoid**: Pastels, corporate colors
**Best For**: Outdoor brands, travel, adventure

### The Sage
**Traits**: Knowledgeable, wise, thoughtful
**Colors**: Deep blue, green, gray, white
**Avoid**: Bright, playful colors
**Best For**: Education, consulting, research

### The Hero
**Traits**: Courageous, bold, determined
**Colors**: Red, black, gold, navy
**Avoid**: Pastels, muted tones
**Best For**: Sports, fitness, achievement

### The Outlaw
**Traits**: Rebellious, disruptive, unconventional
**Colors**: Black, red, electric colors, high contrast
**Avoid**: Soft, corporate colors
**Best For**: Alternative brands, motorcycles, punk

### The Magician
**Traits**: Transformative, visionary, imaginative
**Colors**: Purple, deep blue, gold, mystical tones
**Avoid**: Plain, mundane colors
**Best For**: Tech innovation, entertainment, spirituality

### The Regular Guy/Gal
**Traits**: Relatable, friendly, down-to-earth
**Colors**: Browns, greens, neutral tones, earth colors
**Avoid**: Luxury colors, elitist palette
**Best For**: Home goods, comfort brands, community

### The Lover
**Traits**: Passionate, intimate, sensual
**Colors**: Red, pink, burgundy, rose gold
**Avoid**: Cold, corporate colors
**Best For**: Beauty, fashion, romance

### The Jester
**Traits**: Fun, playful, entertaining
**Colors**: Bright, vibrant, multicolor, yellow, orange
**Avoid**: Serious, muted colors
**Best For**: Entertainment, candy, children

### The Caregiver
**Traits**: Nurturing, compassionate, protective
**Colors**: Soft pink, light blue, green, lavender
**Avoid**: Harsh, aggressive colors
**Best For**: Healthcare, nonprofits, family

### The Creator
**Traits**: Innovative, artistic, visionary
**Colors**: Unique combinations, artistic palettes
**Avoid**: Generic, overused palettes
**Best For**: Design, art, technology

### The Ruler
**Traits**: Authoritative, powerful, successful
**Colors**: Navy, gold, black, burgundy
**Avoid**: Playful, casual colors
**Best For**: Luxury, finance, leadership

---

## Color Emotion Matrix

| Color | Positive Emotions | Negative Emotions | Best For |
|-------|-------------------|-------------------|----------|
| **Red** | Energy, passion, urgency | Aggression, danger | CTAs, sales, food |
| **Orange** | Enthusiasm, creativity | Caution | Youth brands, food |
| **Yellow** | Optimism, warmth | Anxiety (bright) | Attention, happiness |
| **Green** | Growth, health, calm | Envy | Nature, finance, health |
| **Blue** | Trust, calm, professional | Cold, distant | Tech, corporate, health |
| **Purple** | Luxury, creativity | Mysterious | Premium, creative |
| **Pink** | Feminine, playful | Immature | Beauty, children |
| **Brown** | Reliable, earthy | Dull | Organic, outdoors |
| **Black** | Sophisticated, powerful | Oppressive | Luxury, tech |
| **White** | Pure, clean, simple | Sterile | Minimalist, health |
| **Gray** | Neutral, professional | Boring | Corporate, tech |

---

## Industry Color Conventions

### Technology
- **Primary**: Blue (trust, innovation)
- **Accents**: Purple, cyan, green
- **Mood**: Modern, clean, trustworthy
- **Examples**: Blue (IBM, Intel), Purple (Twitch), Green (Spotify)

### Finance
- **Primary**: Blue, green (trust, money)
- **Accents**: Gold (success)
- **Mood**: Trustworthy, stable, professional
- **Examples**: Blue (Chase, PayPal), Green (TD Bank)

### Healthcare
- **Primary**: Blue, green (calm, health)
- **Accents**: White (purity)
- **Mood**: Clean, trustworthy, caring
- **Examples**: Blue (CVS), Green (cross symbol)

### Food & Beverage
- **Primary**: Red, orange, yellow (appetite)
- **Accents**: Green (fresh), brown (natural)
- **Mood**: Appetizing, energetic, warm
- **Examples**: Red (Coca-Cola), Yellow (McDonald's)

### Fashion & Luxury
- **Primary**: Black, gold, white
- **Accents**: Deep burgundy, navy
- **Mood**: Exclusive, sophisticated
- **Examples**: Black (Chanel), Gold (Versace)

### Sustainability
- **Primary**: Green, earth tones
- **Accents**: Blue (water), brown (earth)
- **Mood**: Natural, responsible, authentic
- **Examples**: Green (Whole Foods, Patagonia)

---

## Emotional Goals to Colors

### Trust & Security
```
Primary: oklch(55% 0.15 250)  // Professional blue
Secondary: oklch(45% 0.10 240)  // Deeper blue
Accent: oklch(55% 0.15 145)  // Trustworthy green
```

### Energy & Excitement
```
Primary: oklch(60% 0.22 25)   // Vibrant red
Secondary: oklch(70% 0.20 50) // Energetic orange
Accent: oklch(85% 0.20 95)    // Bright yellow
```

### Calm & Wellness
```
Primary: oklch(55% 0.10 165)  // Sage green
Secondary: oklch(65% 0.08 240) // Soft blue
Accent: oklch(70% 0.06 290)   // Light lavender
```

### Innovation & Tech
```
Primary: oklch(60% 0.20 200)  // Electric cyan
Secondary: oklch(55% 0.20 280) // Deep purple
Accent: oklch(70% 0.25 320)   // Magenta accent
```

### Luxury & Premium
```
Primary: oklch(25% 0.02 60)   // Deep charcoal
Secondary: oklch(70% 0.12 80) // Champagne gold
Accent: oklch(68% 0.10 22)    // Rose gold
```

### Playful & Fun
```
Primary: oklch(55% 0.24 300)  // Electric purple
Secondary: oklch(60% 0.24 350) // Hot pink
Accent: oklch(72% 0.24 130)   // Lime green
```

---

## Context-Based Selection Rules

### B2B / Enterprise
- Prefer: Blue, navy, professional grays
- Avoid: Playful colors, bright accents
- Mood: Trust, stability, professionalism

### B2C / Consumer
- Prefer: Vibrant, engaging colors
- Consider: Brand personality alignment
- Mood: Varies by audience segment

### Creative / Design
- Prefer: Unique, unexpected palettes
- Avoid: Generic corporate colors
- Mood: Artistic, distinctive

### Developer / Technical
- Prefer: Dark modes, high contrast
- Accents: Cyan, green, purple
- Mood: Focused, modern, functional

---

## Cultural Considerations

### Western Markets
- Red: Excitement, passion, danger
- White: Purity, cleanliness
- Blue: Trust, calm

### Eastern Markets
- Red: Luck, prosperity (China)
- White: Mourning (some Asian cultures)
- Gold: Wealth, success

### Universal Safe Choices
- Blue: Generally positive worldwide
- Green: Nature, growth (mostly positive)
- Black: Sophisticated (context-dependent)

---

## Selection Algorithm

```
1. Identify project industry
2. Determine brand archetype
3. Match emotional goals
4. Consider audience culture
5. Select primary color family
6. Build complementary palette
7. Verify accessibility
8. Generate OKLCH values
```
