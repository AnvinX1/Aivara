# Aivara Healthcare Analytics - Frontend

Premium Next.js frontend for the Aivara Healthcare Analytics Platform, built with React, shadcn/ui, Recharts, and GSAP animations.

## Features

- 🎨 **Premium Design**: Modern, healthcare-focused UI with smooth animations
- 📊 **Interactive Charts**: Health marker visualizations using Recharts
- 🤖 **AI Analysis Display**: Beautiful presentation of AI-powered health insights
- 📱 **Responsive**: Fully responsive design for mobile, tablet, and desktop
- ✨ **Smooth Animations**: GSAP-powered animations throughout the app
- 🔐 **Authentication**: Secure JWT-based authentication flow
- 📄 **Report Management**: Upload, view, and analyze medical reports

## Tech Stack

- **Next.js 14+**: React framework with App Router
- **TypeScript**: Type-safe development
- **shadcn/ui**: High-quality React components
- **Recharts**: Charting library for health visualizations
- **GSAP**: Premium animation library
- **Tailwind CSS**: Utility-first CSS framework
- **React Hook Form + Zod**: Form validation
- **Axios**: HTTP client
- **date-fns**: Date formatting utilities
- **lucide-react**: Icon library
- **react-icons**: Additional icons
- **Sonner**: Toast notifications

## Getting Started

### Prerequisites

- Node.js 18+ installed
- Backend API running on `http://localhost:8000`

### Installation

1. Install dependencies:

```bash
cd frontend
npm install
```

2. Create environment file:

```bash
cp .env.local.example .env.local
```

3. Update `.env.local` with your backend API URL if different from default.

### Development

Run the development server:

```bash
npm run dev
```

Open [http://localhost:3000](http://localhost:3000) in your browser.

### Build

Build for production:

```bash
npm run build
```

Start production server:

```bash
npm start
```

## Project Structure

```
frontend/
├── app/                      # Next.js App Router pages
│   ├── (auth)/              # Authentication pages
│   │   ├── login/
│   │   └── register/
│   ├── (dashboard)/         # Protected dashboard routes
│   │   ├── dashboard/
│   │   ├── reports/
│   │   └── reports/[id]/
│   ├── layout.tsx           # Root layout
│   └── globals.css          # Global styles
├── components/
│   ├── ui/                  # shadcn/ui components
│   ├── auth/                # Auth components
│   ├── dashboard/           # Dashboard components
│   └── layout/              # Layout components
├── hooks/                   # Custom React hooks
├── lib/                     # Utilities and API client
├── public/                  # Static assets
└── package.json
```

## Key Components

### Dashboard Components

- **ReportUpload**: Drag-and-drop file upload with progress
- **ReportsList**: Grid view of reports with search
- **ReportDetails**: Detailed report view
- **HealthMarkerChart**: Interactive bar chart for health markers
- **TrendChart**: Line chart showing health trends over time
- **AIAnalysisDisplay**: Display AI analysis results

### Layout Components

- **Header**: Top navigation bar
- **Sidebar**: Side navigation menu

## Features

### Health Marker Visualization

The app provides interactive charts showing:
- Current health marker values vs normal ranges
- Color-coded status (normal, low, high)
- Historical trends over time

### AI Analysis

Display of AI-powered analysis including:
- General health explanations (llama3.2)
- Report reading insights (qwen3-vl:2b)
- Medicine suggestions (medbot)
- Women's health suggestions (edi)

### Animations

GSAP animations include:
- Page transitions
- Component entrance animations
- Hover effects on cards and buttons
- Chart animations on data load

## API Integration

The frontend communicates with the backend API at `NEXT_PUBLIC_API_URL`. See `lib/api.ts` for all API methods.

## Styling

The app uses:
- **Tailwind CSS** for utility classes
- **CSS Variables** for theming (defined in `globals.css`)
- **shadcn/ui** components with custom styling
- **Inter font** from Google Fonts

## Development Tips

- Use `npm run lint` to check for linting errors
- Components use TypeScript for type safety
- GSAP animations are optimized for performance
- Responsive design uses Tailwind breakpoints

## License

Same as the main project.
