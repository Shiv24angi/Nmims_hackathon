"use client";
import * as React from "react";

import {
	motion,
	useMotionTemplate,
	useScroll,
	useTransform,
} from "framer-motion";

export interface ISmoothScrollHeroProps {
	/**
	 * Height of the scroll section in pixels
	 * @default 1500
	 */
	scrollHeight?: number;
	/**
	 * Background image URL for desktop view
	 * @default "https://images.unsplash.com/photo-1511884642898-4c92249e20b6"
	 */
	desktopImage?: string;
	/**
	 * Background image URL for mobile view
	 * @default "https://images.unsplash.com/photo-1511207538754-e8555f2bc187?q=80&w=2412&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D"
	 */
	mobileImage?: string;
	/**
	 * Initial clip path percentage
	 * @default 25
	 */
	initialClipPercentage?: number;
	/**
	 * Final clip path percentage
	 * @default 75
	 */
	finalClipPercentage?: number;
}

interface ISmoothScrollHeroBackgroundProps extends Required<ISmoothScrollHeroProps> {}

const SmoothScrollHeroBackground: React.FC<ISmoothScrollHeroBackgroundProps> = ({
	scrollHeight,
	desktopImage,
	mobileImage,
	initialClipPercentage,
	finalClipPercentage,
}) => {
	const { scrollY } = useScroll();

	const clipStart = useTransform(
		scrollY,
		[0, scrollHeight],
		[initialClipPercentage, 0]
	);
	const clipEnd = useTransform(
		scrollY,
		[0, scrollHeight],
		[finalClipPercentage, 100]
	);

	const clipPath = useMotionTemplate`polygon(${clipStart}% ${clipStart}%, ${clipEnd}% ${clipStart}%, ${clipEnd}% ${clipEnd}%, ${clipStart}% ${clipEnd}%)`;

	const backgroundSize = useTransform(
		scrollY,
		[0, scrollHeight + 500],
		["170%", "100%"]
	);

	return (
		<motion.div
			className="sticky top-0 h-screen w-full bg-black z-0"
			style={{
				clipPath,
				willChange: "transform, opacity",
			}}
		>
			{/* Mobile background */}
			<motion.div
				className="absolute inset-0 md:hidden"
				style={{
					backgroundImage: `url(${mobileImage})`,
					backgroundSize,
					backgroundPosition: "center",
					backgroundRepeat: "no-repeat",
				}}
			/>
			{/* Desktop background */}
			<motion.div
				className="absolute inset-0 hidden md:block"
				style={{
					backgroundImage: `url(${desktopImage})`,
					backgroundSize,
					backgroundPosition: "center",
					backgroundRepeat: "no-repeat",
				}}
			/>
		</motion.div>
	);
};

/**
 * A smooth scroll hero component with parallax background effect
 * @param props - Component props
 * @returns React component
 */
export const SmoothScrollHero: React.FC<ISmoothScrollHeroProps> = ({
	scrollHeight = 1500,
	desktopImage = "https://images.unsplash.com/photo-1543353071-873f17a7a088?q=80&w=2670&auto=format&fit=crop",
	mobileImage = "https://images.unsplash.com/photo-1543353071-873f17a7a088?q=80&w=1000&auto=format&fit=crop",
	initialClipPercentage = 25,
	finalClipPercentage = 75,
}) => {
	return (
		<div
			style={{ height: `calc(${scrollHeight}px + 100vh)` }}
			className="relative w-full"
		>
			<SmoothScrollHeroBackground
				scrollHeight={scrollHeight}
				desktopImage={desktopImage}
				mobileImage={mobileImage}
				initialClipPercentage={initialClipPercentage}
				finalClipPercentage={finalClipPercentage}
			/>
            
            {/* Overlay UI components can go here inside the scrolling Hero container */}
            <div className="absolute inset-0 z-10 pointer-events-none flex flex-col items-center justify-center">
                <h1 className="text-4xl md:text-7xl font-bold text-white text-center drop-shadow-lg tracking-tight">
                    Eat Smarter, <br/><span className="text-green-400">Not Faster</span>
                </h1>
                <p className="mt-6 text-lg md:text-xl text-gray-200 drop-shadow-md text-center max-w-2xl px-4">
                    Your AI-powered cafeteria system that understands your health, habits, and goals.
                </p>
                <div className="mt-8 flex gap-4 pointer-events-auto">
                    <button className="px-6 py-3 bg-green-500 hover:bg-green-600 text-white rounded-lg font-medium transition-all shadow-lg">
                        Login to System
                    </button>
                    <button className="px-6 py-3 bg-white/10 hover:bg-white/20 backdrop-blur-md text-white border border-white/20 rounded-lg font-medium transition-all shadow-lg">
                        Create Account
                    </button>
                </div>
            </div>
		</div>
	);
};

export default SmoothScrollHero;
