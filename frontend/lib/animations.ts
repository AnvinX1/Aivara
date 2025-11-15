import { gsap } from 'gsap';

/**
 * Fade in animation
 */
export const fadeIn = (element: HTMLElement, delay = 0) => {
  gsap.fromTo(
    element,
    { opacity: 0, y: 20 },
    { opacity: 1, y: 0, duration: 0.6, ease: 'power3.out', delay }
  );
};

/**
 * Stagger fade in for multiple elements
 */
export const staggerFadeIn = (elements: HTMLElement[], stagger = 0.1) => {
  gsap.fromTo(
    elements,
    { opacity: 0, y: 30, scale: 0.95 },
    {
      opacity: 1,
      y: 0,
      scale: 1,
      duration: 0.5,
      ease: 'power3.out',
      stagger,
    }
  );
};

/**
 * Slide in from left
 */
export const slideInLeft = (element: HTMLElement, delay = 0) => {
  gsap.fromTo(
    element,
    { opacity: 0, x: -50 },
    { opacity: 1, x: 0, duration: 0.6, ease: 'power3.out', delay }
  );
};

/**
 * Slide in from right
 */
export const slideInRight = (element: HTMLElement, delay = 0) => {
  gsap.fromTo(
    element,
    { opacity: 0, x: 50 },
    { opacity: 1, x: 0, duration: 0.6, ease: 'power3.out', delay }
  );
};

/**
 * Scale up animation
 */
export const scaleUp = (element: HTMLElement, delay = 0) => {
  gsap.fromTo(
    element,
    { opacity: 0, scale: 0.8 },
    { opacity: 1, scale: 1, duration: 0.5, ease: 'back.out(1.7)', delay }
  );
};

/**
 * Hover lift effect
 */
export const hoverLift = (element: HTMLElement) => {
  const handleMouseEnter = () => {
    gsap.to(element, { y: -4, scale: 1.02, duration: 0.3, ease: 'power2.out' });
  };
  const handleMouseLeave = () => {
    gsap.to(element, { y: 0, scale: 1, duration: 0.3, ease: 'power2.out' });
  };

  element.addEventListener('mouseenter', handleMouseEnter);
  element.addEventListener('mouseleave', handleMouseLeave);

  return () => {
    element.removeEventListener('mouseenter', handleMouseEnter);
    element.removeEventListener('mouseleave', handleMouseLeave);
  };
};

/**
 * Pulse animation
 */
export const pulse = (element: HTMLElement) => {
  return gsap.to(element, {
    scale: 1.05,
    duration: 1,
    repeat: -1,
    yoyo: true,
    ease: 'power1.inOut',
  });
};

/**
 * Page transition
 */
export const pageTransition = (element: HTMLElement) => {
  return gsap.fromTo(
    element,
    { opacity: 0, y: 20 },
    { opacity: 1, y: 0, duration: 0.6, ease: 'power3.out' }
  );
};

