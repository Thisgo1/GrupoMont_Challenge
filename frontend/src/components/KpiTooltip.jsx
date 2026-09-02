import { Info } from "lucide-react";
import {
  Tooltip,
  TooltipContent,
  TooltipProvider,
  TooltipTrigger,
} from "@/components/ui/tooltip";

export default function KpiTooltip({ label, description, formula, children }) {
  return (
    <TooltipProvider>
      <Tooltip delayDuration={200}>
        <TooltipTrigger asChild>
          <div className="group inline-flex items-center gap-1 cursor-help">
            {children}
            <Info className="h-3.5 w-3.5 text-muted-foreground opacity-60 group-hover:opacity-100 transition-opacity flex-shrink-0" />
          </div>
        </TooltipTrigger>
        <TooltipContent
          side="top"
          align="center"
          className="max-w-xs min-w-[200px] p-4 bg-slate-300 dark:bg-gray-800 border border-gray-200 dark:border-gray-700 shadow-lg rounded-lg"
        >
          <p className="font-semibold text-sm text-gray-900 dark:text-white">{label}</p>
          <p className="text-xs text-gray-600 dark:text-gray-300 mt-1 leading-relaxed">
            {description}
          </p>
          {formula && (
            <div className="mt-2 pt-2 border-t border-gray-200 dark:border-gray-700">
              <p className="text-xs font-mono bg-gray-100 dark:bg-gray-900 p-1.5 rounded text-gray-700 dark:text-gray-300 break-all">
                {formula}
              </p>
            </div>
          )}
        </TooltipContent>
      </Tooltip>
    </TooltipProvider>
  );
}
