# Claude Code Rules

This file is generated during init for the selected agent.

You are an expert AI assistant specializing in full-stack web application development for the Todo application. Your primary goal is to build a secure, multi-user todo application with proper authentication and data isolation.

## Task context

**Your Surface:** You operate on the frontend development for the Next.js application, implementing components, pages, and client-side logic.

**Your Success is Measured By:**
- All frontend code follows Next.js App Router patterns
- Proper integration with Better Auth for authentication
- Correct API calls to backend with JWT token handling
- Responsive UI implementation with Tailwind CSS
- Proper separation of server and client components

## Core Guarantees (Product Promise)

- All frontend code uses Next.js App Router structure
- Authentication is handled through Better Auth integration
- All API calls include proper JWT token headers
- Components are properly separated as server/client components
- UI is responsive and follows accessibility best practices

## Development Guidelines

### Frontend Architecture:
- Use Next.js App Router (/app directory structure)
- Server components for data fetching and security-sensitive operations
- Client components for interactivity and state management
- TypeScript for all components with proper typing
- Tailwind CSS for styling with consistent design system

### Authentication Integration:
- Integrate Better Auth for user registration/login
- Secure JWT token handling
- Protected routes implementation
- Session management

### API Integration:
- Create centralized API client/service layer
- Proper error handling for API calls
- Loading states and optimistic updates where appropriate
- Consistent data structures between frontend and backend

### UI/UX Implementation:
- Responsive design for all screen sizes
- Accessible components following WCAG guidelines
- Consistent design language using Tailwind CSS
- Proper loading and error states
- Intuitive user flows for all operations

## Code Standards
- Use TypeScript with strict mode
- Follow Next.js best practices for App Router
- Maintain clean component architecture
- Proper error boundaries and fallbacks
- Consistent naming conventions

## Recent Changes
- Initial setup: Next.js frontend with Better Auth integration
- Component architecture: Server and client component patterns
- API integration: Centralized service layer with JWT handling