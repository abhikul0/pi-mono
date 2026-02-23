/**
 * Permission Gate Extension
 *
 * Prompts for confirmation before running potentially dangerous bash commands.
 * Patterns checked: rm -rf, sudo, chmod/chown 777
 */

import type { ExtensionAPI } from "@mariozechner/pi-coding-agent";

export default function (pi: ExtensionAPI) {
	// const dangerousPatterns = [/\brm\s+(-rf?|--recursive)/i, /\bsudo\b/i, /\b(chmod|chown)\b.*777/i];
	const dangerousPatterns = [
			// General Linux/Unix dangers
			/\brm\s+(-rf?|--recursive)/i, 
			/\brm\b/i, 
			/\bsudo\b/i, 
			/\b(chmod|chown)\b.*777/i,
			/\bdd\b.*\b(dev|\/dev)\//i,
			/\b(mv|cp)\b.*\//i,
			/:.*\(\).*:\|.*&.*;/,
			/\b(wget|curl)\b.*\|.*(sh|bash|\/bin\/)/i,
			
			// macOS-specific dangerous patterns
			/\bdiskutil\b.*\berase/i,           // diskutil eraseVolume / diskutil eraseDisk
			/\bhdiutil\b.*\berase/i,             // hdiutil erase (DMG/disk image destruction)
			/\brm\b.*~\//i,                      // rm -rf ~/, rm ~/ (home directory deletion)
			/\bopen\b.*\/Applications\/\*.*\.app/i, // open /Applications/*.app (app spam)
			/\bmkfs\./i,                         // mkfs.* (filesystem formatting)
			/\bdiskutil\b.*\bzero/i              // diskutil zeroDisk (zeroing drives)
		];

	pi.on("tool_call", async (event, ctx) => {
		if (event.toolName !== "bash") return undefined;

		const command = event.input.command as string;
		const isDangerous = dangerousPatterns.some((p) => p.test(command));

		if (isDangerous) {
			if (!ctx.hasUI) {
				// In non-interactive mode, block by default
				return { block: true, reason: "Dangerous command blocked (no UI for confirmation)" };
			}

			const choice = await ctx.ui.select(`⚠️ Dangerous command:\n\n  ${command}\n\nAllow?`, ["Yes", "No"]);

			if (choice !== "Yes") {
				return { block: true, reason: "Blocked by user" };
			}
		}

		return undefined;
	});
}
